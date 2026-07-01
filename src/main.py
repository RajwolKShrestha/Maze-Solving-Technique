"""Starter entrypoint for the maze visualizer."""

from __future__ import annotations

try:
    import pygame
except ImportError as exc:  # pragma: no cover - runtime guard
    raise RuntimeError("pygame is required to run the visualizer. Install it with 'pip install pygame'.") from exc

from src.core.constants import COLORS
from src.generators.presets import get_preset_maze, list_preset_names
from src.visualization.renderer import draw_maze


def main() -> None:
    """Open a simple window and render one preset maze."""

    pygame.init()

    preset_name = list_preset_names()[2]
    maze = get_preset_maze(preset_name)
    cell_size = 40
    margin = 20
    width = maze.cols * cell_size + margin * 2
    height = maze.rows * cell_size + margin * 2

    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Maze Solving Technique - {preset_name}")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill(COLORS["light_gray"])
        draw_maze(
            screen,
            maze,
            cell_size=cell_size,
            origin=(margin, margin),
            start=(0, 0),
            goal=(maze.rows - 1, maze.cols - 1),
        )
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()