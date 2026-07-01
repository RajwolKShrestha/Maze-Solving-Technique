"""Tests for maze generation and preset mazes."""

from __future__ import annotations

import sys
from collections import deque
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.maze import Maze
from src.generators.maze_generator import generate_perfect_maze
from src.generators.presets import get_preset_maze, list_preset_names


class TestMazeGeneration(unittest.TestCase):
    def test_generated_maze_has_expected_dimensions(self) -> None:
        maze = generate_perfect_maze(6, 7, seed=123)
        self.assertEqual(maze.rows, 6)
        self.assertEqual(maze.cols, 7)

    def test_generated_maze_is_bidirectionally_valid(self) -> None:
        maze = generate_perfect_maze(8, 8, seed=7)
        self.assertTrue(maze.validate_maze())

    def test_generated_maze_is_fully_reachable(self) -> None:
        maze = generate_perfect_maze(6, 6, seed=99)
        visited = self._reachable_cells(maze, (0, 0))
        self.assertEqual(len(visited), maze.rows * maze.cols)

    def test_generation_is_deterministic_for_same_seed(self) -> None:
        maze_a = generate_perfect_maze(5, 5, seed=42)
        maze_b = generate_perfect_maze(5, 5, seed=42)
        self.assertEqual(maze_a.walls, maze_b.walls)

    def test_generation_differs_for_different_seeds(self) -> None:
        maze_a = generate_perfect_maze(5, 5, seed=1)
        maze_b = generate_perfect_maze(5, 5, seed=2)
        self.assertNotEqual(maze_a.walls, maze_b.walls)

    def test_preset_mazes_exist(self) -> None:
        presets = list_preset_names()
        self.assertGreaterEqual(len(presets), 5)
        for name in presets:
            maze = get_preset_maze(name)
            self.assertIsInstance(maze, Maze)
            self.assertTrue(maze.validate_maze())

    def _reachable_cells(self, maze: Maze, start: tuple[int, int]) -> set[tuple[int, int]]:
        visited = {start}
        queue = deque([start])

        while queue:
            row, col = queue.popleft()
            for neighbor in maze.get_neighbors(row, col):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited


if __name__ == "__main__":
    unittest.main()