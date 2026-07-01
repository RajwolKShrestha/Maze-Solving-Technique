"""Pygame rendering helpers for maze visualization."""

from __future__ import annotations

from typing import Iterable, Sequence, Tuple

try:
    import pygame
except ImportError:  # pragma: no cover - import guard for non-graphical environments
    pygame = None

from src.core.constants import COLORS, EAST, NORTH, SOUTH, WEST
from src.core.maze import Maze

Cell = Tuple[int, int]


def _require_pygame() -> None:
    if pygame is None:
        raise RuntimeError("pygame is required for rendering; install it with 'pip install pygame'")


def draw_maze(
    screen,
    maze: Maze,
    cell_size: int = 40,
    origin: tuple[int, int] = (0, 0),
    wall_color: tuple[int, int, int] | None = None,
    wall_thickness: int = 2,
    background_color: tuple[int, int, int] | None = None,
    start: Cell | None = None,
    goal: Cell | None = None,
) -> None:
    """Draw maze walls and optional start/goal markers."""

    _require_pygame()

    wall_color = wall_color or COLORS["black"]
    background_color = background_color or COLORS["white"]
    origin_x, origin_y = origin

    for row in range(maze.rows):
        for col in range(maze.cols):
            cell_left = origin_x + col * cell_size
            cell_top = origin_y + row * cell_size
            cell_rect = pygame.Rect(cell_left, cell_top, cell_size, cell_size)
            pygame.draw.rect(screen, background_color, cell_rect)

            if maze.has_wall(row, col, NORTH):
                pygame.draw.line(
                    screen,
                    wall_color,
                    (cell_left, cell_top),
                    (cell_left + cell_size, cell_top),
                    wall_thickness,
                )
            if maze.has_wall(row, col, SOUTH):
                pygame.draw.line(
                    screen,
                    wall_color,
                    (cell_left, cell_top + cell_size),
                    (cell_left + cell_size, cell_top + cell_size),
                    wall_thickness,
                )
            if maze.has_wall(row, col, EAST):
                pygame.draw.line(
                    screen,
                    wall_color,
                    (cell_left + cell_size, cell_top),
                    (cell_left + cell_size, cell_top + cell_size),
                    wall_thickness,
                )
            if maze.has_wall(row, col, WEST):
                pygame.draw.line(
                    screen,
                    wall_color,
                    (cell_left, cell_top),
                    (cell_left, cell_top + cell_size),
                    wall_thickness,
                )

    if start is not None:
        draw_cell_fill(screen, start, cell_size, origin, COLORS["green"])
    if goal is not None:
        draw_cell_fill(screen, goal, cell_size, origin, COLORS["red"])


def draw_cell_fill(
    screen,
    cell: Cell,
    cell_size: int,
    origin: tuple[int, int],
    color: tuple[int, int, int],
) -> None:
    """Fill a single cell with a color."""

    _require_pygame()
    row, col = cell
    origin_x, origin_y = origin
    padding = max(2, cell_size // 8)
    cell_left = origin_x + col * cell_size + padding
    cell_top = origin_y + row * cell_size + padding
    size = cell_size - 2 * padding
    pygame.draw.rect(screen, color, pygame.Rect(cell_left, cell_top, size, size))


def draw_visited_cells(
    screen,
    cells: Iterable[Cell],
    cell_size: int,
    origin: tuple[int, int] = (0, 0),
    color: tuple[int, int, int] | None = None,
) -> None:
    """Highlight a sequence of visited cells."""

    _require_pygame()
    color = color or COLORS["light_blue"]
    for cell in cells:
        draw_cell_fill(screen, cell, cell_size, origin, color)


def draw_path(
    screen,
    path: Sequence[Cell],
    cell_size: int,
    origin: tuple[int, int] = (0, 0),
    color: tuple[int, int, int] | None = None,
) -> None:
    """Highlight the final solution path."""

    _require_pygame()
    color = color or COLORS["yellow"]
    for cell in path:
        draw_cell_fill(screen, cell, cell_size, origin, color)