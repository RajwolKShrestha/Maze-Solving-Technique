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


def draw_flood_fill_heatmap(
    screen,
    distances: Sequence[Sequence[float]],
    cell_size: int,
    origin: tuple[int, int] = (0, 0),
    max_opacity: int = 190,
) -> None:
    """Overlay a heatmap for flood-fill distances."""

    _require_pygame()
    origin_x, origin_y = origin
    finite_values = [value for row in distances for value in row if value != float("inf")]
    if not finite_values:
        return

    max_distance = max(finite_values)
    if max_distance == 0:
        max_distance = 1

    overlay = pygame.Surface((cell_size, cell_size), pygame.SRCALPHA)
    for row_index, row in enumerate(distances):
        for col_index, distance in enumerate(row):
            if distance == float("inf"):
                continue

            ratio = distance / max_distance
            red = int(60 + 180 * ratio)
            blue = int(220 - 160 * ratio)
            alpha = int(max_opacity * (1.0 - ratio * 0.55))
            overlay.fill((red, 90, blue, alpha))
            screen.blit(
                overlay,
                (origin_x + col_index * cell_size, origin_y + row_index * cell_size),
            )


def draw_wall_bitmask_overlay(
    screen,
    maze: Maze,
    cell_size: int,
    origin: tuple[int, int] = (0, 0),
    font=None,
) -> None:
    """Render the 4-bit wall state of each cell on top of the maze."""

    _require_pygame()
    if font is None:
        font = pygame.font.SysFont("arial", max(12, cell_size // 4))

    origin_x, origin_y = origin
    for row in range(maze.rows):
        for col in range(maze.cols):
            bitmask = maze.get_wall_state(row, col)
            label = font.render(f"{bitmask:04b}", True, COLORS["dark_gray"])
            label_rect = label.get_rect(
                center=(
                    origin_x + col * cell_size + cell_size // 2,
                    origin_y + row * cell_size + cell_size // 2,
                )
            )
            screen.blit(label, label_rect)