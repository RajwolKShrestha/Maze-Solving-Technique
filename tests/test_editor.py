"""Tests for the maze editor and save/load helpers."""

from __future__ import annotations

import sys
from pathlib import Path
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.constants import EAST, NORTH
from src.editor.maze_editor import MazeEditor
from src.utils.file_handler import load_maze_from_file, save_maze_to_file


class TestMazeEditor(unittest.TestCase):
    def test_toggle_wall_changes_state(self) -> None:
        editor = MazeEditor(4, 4)
        self.assertTrue(editor.maze.has_wall(0, 0, NORTH))
        editor.toggle_wall(0, 0, NORTH)
        self.assertFalse(editor.maze.has_wall(0, 0, NORTH))

    def test_add_passage_connects_cells(self) -> None:
        editor = MazeEditor(4, 4)
        self.assertTrue(editor.add_passage(1, 1, 1, 2))
        self.assertFalse(editor.maze.has_wall(1, 1, EAST))
        self.assertFalse(editor.maze.has_wall(1, 2, WEST := 0b0001))

    def test_save_and_load_round_trip(self) -> None:
        editor = MazeEditor(3, 3)
        editor.add_passage(0, 0, 0, 1)
        editor.add_passage(0, 1, 1, 1)

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = Path(temp_dir) / "maze.txt"
            editor.save(str(file_path))

            loaded = load_maze_from_file(file_path)

        self.assertEqual(loaded.rows, 3)
        self.assertEqual(loaded.cols, 3)
        self.assertEqual(loaded.walls, editor.maze.walls)

    def test_reset_restores_full_walls(self) -> None:
        editor = MazeEditor(3, 3)
        editor.add_passage(0, 0, 0, 1)
        editor.reset()
        self.assertTrue(editor.maze.has_wall(0, 0, NORTH))

    def test_cell_from_pixel(self) -> None:
        editor = MazeEditor(5, 5, cell_size=20)
        self.assertEqual(editor.cell_from_pixel(41, 39), (1, 2))

    def test_edge_from_pixel(self) -> None:
        editor = MazeEditor(5, 5, cell_size=20)
        self.assertEqual(editor.edge_from_pixel(9, 2), NORTH)

    def test_is_valid(self) -> None:
        editor = MazeEditor(3, 3)
        self.assertTrue(editor.is_valid())


if __name__ == "__main__":
    unittest.main()