"""Maze file save/load helpers."""

from __future__ import annotations

from pathlib import Path

from src.core.maze import Maze


def save_maze_to_file(maze: Maze, file_path: str | Path) -> None:
    """Save a maze as a simple text format.

    Format:
    - first line: rows,cols
    - subsequent lines: comma-separated wall bitmasks per row
    """

    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with path.open("w", encoding="utf-8") as file_handle:
        file_handle.write(f"{maze.rows},{maze.cols}\n")
        for row in maze.walls:
            file_handle.write(",".join(str(cell) for cell in row) + "\n")


def load_maze_from_file(file_path: str | Path) -> Maze:
    """Load a maze previously saved by `save_maze_to_file`."""

    path = Path(file_path)
    with path.open("r", encoding="utf-8") as file_handle:
        rows_text, cols_text = file_handle.readline().strip().split(",")
        rows = int(rows_text)
        cols = int(cols_text)
        maze = Maze(rows, cols, all_walls=False)

        for row_index in range(rows):
            values = file_handle.readline().strip().split(",")
            if len(values) != cols:
                raise ValueError("Invalid maze file: row length does not match header")
            maze.walls[row_index] = [int(value) for value in values]

    if not maze.validate_maze():
        raise ValueError("Invalid maze file: inconsistent wall data")

    return maze