"""Interactive maze editing helpers."""

from __future__ import annotations

from src.core.constants import EAST, NORTH, SOUTH, WEST
from src.core.maze import Maze
from src.utils.file_handler import load_maze_from_file, save_maze_to_file


class MazeEditor:
    """A light-weight maze editor API for toggling walls and persisting mazes."""

    def __init__(self, rows: int, cols: int, cell_size: int = 40):
        self.cell_size = cell_size
        self.maze = Maze(rows, cols, all_walls=True)

    def toggle_wall(self, row: int, col: int, direction: int) -> bool:
        """Toggle a wall and keep adjacent cells consistent when possible."""

        if self.maze.has_wall(row, col, direction):
            self.maze.remove_wall(row, col, direction)
        else:
            self.maze.add_wall(row, col, direction)

        return True

    def add_passage(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """Remove the wall between two adjacent cells."""

        return self.maze.connect_cells(row1, col1, row2, col2)

    def reset(self) -> None:
        """Reset the editor to a fully walled maze."""

        self.maze = Maze(self.maze.rows, self.maze.cols, all_walls=True)

    def save(self, file_path: str) -> None:
        """Save the current maze state to disk."""

        save_maze_to_file(self.maze, file_path)

    def load(self, file_path: str) -> None:
        """Load a maze from disk into the editor."""

        self.maze = load_maze_from_file(file_path)

    def cell_from_pixel(self, x: int, y: int) -> tuple[int, int]:
        """Convert screen coordinates to a maze cell."""

        return y // self.cell_size, x // self.cell_size

    def edge_from_pixel(self, x: int, y: int) -> int | None:
        """Infer the nearest edge from a click position within a cell."""

        offset_x = x % self.cell_size
        offset_y = y % self.cell_size
        edge_margin = max(4, self.cell_size // 8)

        if offset_y <= edge_margin:
            return NORTH
        if offset_y >= self.cell_size - edge_margin:
            return SOUTH
        if offset_x <= edge_margin:
            return WEST
        if offset_x >= self.cell_size - edge_margin:
            return EAST
        return None

    def is_valid(self) -> bool:
        """Check that the current maze state is consistent."""

        return self.maze.validate_maze()