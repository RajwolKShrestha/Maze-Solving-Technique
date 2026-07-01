"""Starter entrypoint for the maze visualizer."""

from __future__ import annotations

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
from src.visualization.ui_elements import AlgorithmSelector, MetricsPanel, PlaybackControls


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

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Maze Solving Technique - {preset_name}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("arial", 20)
    running = True

    solver = ALGORITHM_CLASSES["BFS"](maze, (0, 0), (maze.rows - 1, maze.cols - 1))
    solver.solve()
    animator = Animator(solver.explored, solver.path)
    algorithm_selector = AlgorithmSelector(list(ALGORITHM_CLASSES.keys()), panel_x, 30)
    playback_controls = PlaybackControls(panel_x, 90)
    metrics_panel = MetricsPanel(panel_x, 150)
    metrics_panel.update(solver)
    comparison_panel = ComparisonPanel(panel_x, 410)
    comparison_snapshots = run_comparison(maze, (0, 0), (maze.rows - 1, maze.cols - 1), ALGORITHM_CLASSES)
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

        if animator.is_playing:
            animator.step_forward()
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
        metrics_panel.draw(screen, font)
        comparison_panel.draw(screen, font)

        header = font.render(f"Preset: {preset_name}", True, COLORS["black"])
        screen.blit(header, (panel_x, height - 40))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()