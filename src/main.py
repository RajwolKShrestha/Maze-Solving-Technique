"""Starter entrypoint for the maze visualizer."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

try:
    import pygame
except ImportError as exc:  # pragma: no cover - runtime guard
    raise RuntimeError("pygame is required to run the visualizer. Install it with 'pip install pygame'.") from exc

from src.algorithms import AStar, BFS, DFS, Dijkstra, FloodFill
from src.core.constants import COLORS
from src.generators.presets import get_preset_maze, list_preset_names
from src.visualization.comparison import rank_by_path_then_steps, run_comparison
from src.visualization.comparison_panel import ComparisonPanel
from src.visualization.animator import Animator
from src.visualization.renderer import draw_flood_fill_heatmap, draw_maze, draw_path, draw_visited_cells, draw_wall_bitmask_overlay
from src.visualization.ui_elements import AlgorithmSelector, MetricsPanel, PlaybackControls, SpeedControl, ViewModeControls


ALGORITHM_CLASSES = {
    "BFS": BFS,
    "DFS": DFS,
    "Dijkstra": Dijkstra,
    "A*": AStar,
    "Flood Fill": FloodFill,
}


def main() -> None:
    """Open the maze visualizer with controls and metrics."""

    pygame.init()

    preset_name = list_preset_names()[2]
    maze = get_preset_maze(preset_name)
    cell_size = 40
    margin = 20
    maze_width = maze.cols * cell_size + margin * 2
    panel_x = maze_width + 20
    width = maze_width + 290
    height = maze.rows * cell_size + margin * 2

    is_fullscreen = False
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Maze Solving Technique - {preset_name}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    running = True
    movement_delay_ms = 120
    last_step_tick = pygame.time.get_ticks()

    solver = ALGORITHM_CLASSES["BFS"](maze, (0, 0), (maze.rows - 1, maze.cols - 1))
    solver.solve()
    animator = Animator(solver.explored, solver.path)
    algorithm_selector = AlgorithmSelector(list(ALGORITHM_CLASSES.keys()), panel_x, 30)
    playback_controls = PlaybackControls(panel_x, 90)
    speed_control = SpeedControl(panel_x, 150, initial_delay_ms=movement_delay_ms)
    view_mode_controls = ViewModeControls(panel_x, 190)
    metrics_panel = MetricsPanel(panel_x, 240)
    metrics_panel.update(solver)
    comparison_panel = ComparisonPanel(panel_x, 500)
    comparison_snapshots = run_comparison(maze, (0, 0), (maze.rows - 1, maze.cols - 1), ALGORITHM_CLASSES)
    comparison_panel.update(rank_by_path_then_steps(comparison_snapshots))

    def apply_display_mode(fullscreen: bool) -> None:
        nonlocal screen, width, height, panel_x, algorithm_selector, playback_controls, speed_control, view_mode_controls, metrics_panel, comparison_panel

        is_desktop_fullscreen = fullscreen
        if is_desktop_fullscreen:
            info = pygame.display.Info()
            width = info.current_w
            height = info.current_h
            screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
        else:
            width = maze_width + 290
            height = maze.rows * cell_size + margin * 2
            screen = pygame.display.set_mode((width, height))

        panel_x = maze_width + 20
        algorithm_selector = AlgorithmSelector(list(ALGORITHM_CLASSES.keys()), panel_x, 30)
        playback_controls = PlaybackControls(panel_x, 90)
        speed_control = SpeedControl(panel_x, 150, initial_delay_ms=movement_delay_ms)
        view_mode_controls = ViewModeControls(panel_x, 190)
        metrics_panel = MetricsPanel(panel_x, 240)
        metrics_panel.update(solver)
        comparison_panel = ComparisonPanel(panel_x, 500)
        comparison_panel.update(rank_by_path_then_steps(comparison_snapshots))

    def rebuild_solver(selected_name: str) -> None:
        nonlocal solver, animator
        solver = ALGORITHM_CLASSES[selected_name](maze, (0, 0), (maze.rows - 1, maze.cols - 1))
        solver.solve()
        animator = Animator(solver.explored, solver.path)
        metrics_panel.update(solver)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = event.pos
                selected_algorithm = algorithm_selector.handle_click(click)
                if selected_algorithm is not None:
                    rebuild_solver(selected_algorithm)
                    continue

                action = playback_controls.handle_click(click)
                if action == "play":
                    animator.is_playing = True
                elif action == "pause":
                    animator.is_playing = False
                elif action == "reset":
                    animator.reset()

                new_delay = speed_control.handle_click(click)
                if new_delay is not None:
                    movement_delay_ms = new_delay

                display_action = view_mode_controls.handle_click(click)
                if display_action == "fullscreen" and not is_fullscreen:
                    is_fullscreen = True
                    apply_display_mode(True)
                elif display_action == "windowed" and is_fullscreen:
                    is_fullscreen = False
                    apply_display_mode(False)

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    is_fullscreen = not is_fullscreen
                    apply_display_mode(is_fullscreen)

        now = pygame.time.get_ticks()
        if animator.is_playing and now - last_step_tick >= movement_delay_ms:
            if animator.step_forward():
                last_step_tick = now
            if animator.completed_explored():
                animator.is_playing = False

        screen.fill(COLORS["light_gray"])
        draw_maze(
            screen,
            maze,
            cell_size=cell_size,
            origin=(margin, margin),
            start=(0, 0),
            goal=(maze.rows - 1, maze.cols - 1),
        )
        if solver.name == "Flood Fill" and hasattr(solver, "distances"):
            draw_flood_fill_heatmap(screen, solver.distances, cell_size, origin=(margin, margin))
        draw_wall_bitmask_overlay(screen, maze, cell_size, origin=(margin, margin), font=font)
        draw_visited_cells(screen, animator.visible_explored(), cell_size, origin=(margin, margin))
        draw_path(screen, animator.visible_path(), cell_size, origin=(margin, margin))

        pygame.draw.line(screen, COLORS["dark_gray"], (maze_width + 10, 10), (maze_width + 10, height - 10), 2)
        algorithm_selector.draw(screen, font)
        playback_controls.draw(screen, font, animator.is_playing)
        speed_control.draw(screen, font)
        view_mode_controls.draw(screen, font, is_fullscreen)
        metrics_panel.draw(screen, font)
        comparison_panel.draw(screen, font)

        header = font.render(f"Preset: {preset_name}", True, COLORS["black"])
        screen.blit(header, (panel_x, height - 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()