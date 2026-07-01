"""Random maze generation utilities."""

from __future__ import annotations

import random
from typing import Optional, Tuple

from src.core.constants import DIRECTIONS, DIRECTION_MAP
from src.core.maze import Maze

Cell = Tuple[int, int]


def _unvisited_neighbors(
    row: int,
    col: int,
    rows: int,
    cols: int,
    visited: list[list[bool]],
) -> list[tuple[int, int, int]]:
    neighbors: list[tuple[int, int, int]] = []
    for direction in DIRECTIONS:
        delta_row, delta_col = DIRECTION_MAP[direction]
        next_row = row + delta_row
        next_col = col + delta_col
        if 0 <= next_row < rows and 0 <= next_col < cols and not visited[next_row][next_col]:
            neighbors.append((next_row, next_col, direction))
    return neighbors


def generate_perfect_maze(
    rows: int,
    cols: int,
    seed: Optional[int] = None,
    start: Cell = (0, 0),
) -> Maze:
    """Generate a perfect maze using randomized depth-first search."""

    if rows <= 0 or cols <= 0:
        raise ValueError("rows and cols must be positive integers")

    start_row, start_col = start
    if not (0 <= start_row < rows and 0 <= start_col < cols):
        raise ValueError("start cell must be inside the maze bounds")

    rng = random.Random(seed)
    maze = Maze(rows, cols, all_walls=True)
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    stack: list[Cell] = [start]
    visited[start_row][start_col] = True

    while stack:
        row, col = stack[-1]
        neighbors = _unvisited_neighbors(row, col, rows, cols, visited)
        rng.shuffle(neighbors)

        if neighbors:
            next_row, next_col, _ = neighbors[0]
            maze.connect_cells(row, col, next_row, next_col)
            visited[next_row][next_col] = True
            stack.append((next_row, next_col))
        else:
            stack.pop()

    return maze