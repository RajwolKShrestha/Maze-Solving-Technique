"""Tests for BFS and DFS maze solvers."""

from __future__ import annotations

import sys
from collections import deque
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms.bfs import BFS
from src.algorithms.astar import AStar
from src.algorithms.dfs import DFS
from src.algorithms.dijkstra import Dijkstra
from src.algorithms.flood_fill import FloodFill
from src.core.maze import Maze
from src.generators.maze_generator import generate_perfect_maze


class TestSolverAlgorithms(unittest.TestCase):
    def setUp(self) -> None:
        self.open_maze = Maze(3, 3, all_walls=False)
        self.generated_maze = generate_perfect_maze(6, 6, seed=21)

    def test_bfs_finds_shortest_path_in_open_grid(self) -> None:
        solver = BFS(self.open_maze, (0, 0), (2, 2))
        self.assertTrue(solver.solve())
        self.assertEqual(solver.path[0], (0, 0))
        self.assertEqual(solver.path[-1], (2, 2))
        self.assertEqual(len(solver.path), 5)
        self.assertTrue(self._path_is_valid(self.open_maze, solver.path))

    def test_bfs_finds_path_in_generated_maze(self) -> None:
        solver = BFS(self.generated_maze, (0, 0), (5, 5))
        self.assertTrue(solver.solve())
        self.assertTrue(self._path_is_valid(self.generated_maze, solver.path))
        self.assertEqual(solver.path[0], (0, 0))
        self.assertEqual(solver.path[-1], (5, 5))

    def test_dfs_finds_path_in_generated_maze(self) -> None:
        solver = DFS(self.generated_maze, (0, 0), (5, 5))
        self.assertTrue(solver.solve())
        self.assertTrue(self._path_is_valid(self.generated_maze, solver.path))
        self.assertEqual(solver.path[0], (0, 0))
        self.assertEqual(solver.path[-1], (5, 5))

    def test_dfs_path_is_not_shorter_than_bfs_on_open_grid(self) -> None:
        bfs_solver = BFS(self.open_maze, (0, 0), (2, 2))
        dfs_solver = DFS(self.open_maze, (0, 0), (2, 2))

        self.assertTrue(bfs_solver.solve())
        self.assertTrue(dfs_solver.solve())
        self.assertGreaterEqual(len(dfs_solver.path), len(bfs_solver.path))

    def test_unsolvable_maze_returns_false(self) -> None:
        blocked_maze = Maze(2, 2, all_walls=True)
        solver = BFS(blocked_maze, (0, 0), (1, 1))
        self.assertFalse(solver.solve())
        self.assertEqual(solver.path, [])

    def test_metrics_exposed_by_solver(self) -> None:
        solver = BFS(self.generated_maze, (0, 0), (5, 5))
        self.assertTrue(solver.solve())
        metrics = solver.get_metrics()
        self.assertEqual(metrics["algorithm"], "BFS")
        self.assertEqual(metrics["path_length"], len(solver.path))
        self.assertGreater(metrics["steps"], 0)

    def test_dijkstra_matches_bfs_on_open_grid(self) -> None:
        bfs_solver = BFS(self.open_maze, (0, 0), (2, 2))
        dijkstra_solver = Dijkstra(self.open_maze, (0, 0), (2, 2))

        self.assertTrue(bfs_solver.solve())
        self.assertTrue(dijkstra_solver.solve())
        self.assertEqual(len(dijkstra_solver.path), len(bfs_solver.path))
        self.assertTrue(self._path_is_valid(self.open_maze, dijkstra_solver.path))

    def test_astar_finds_valid_path(self) -> None:
        solver = AStar(self.generated_maze, (0, 0), (5, 5))
        self.assertTrue(solver.solve())
        self.assertTrue(self._path_is_valid(self.generated_maze, solver.path))
        self.assertEqual(solver.path[0], (0, 0))
        self.assertEqual(solver.path[-1], (5, 5))

    def test_flood_fill_finds_valid_path(self) -> None:
        solver = FloodFill(self.generated_maze, (0, 0), (5, 5))
        self.assertTrue(solver.solve())
        self.assertTrue(self._path_is_valid(self.generated_maze, solver.path))
        self.assertEqual(solver.path[0], (0, 0))
        self.assertEqual(solver.path[-1], (5, 5))

    def test_flood_fill_distance_matches_path_length_minus_one(self) -> None:
        solver = FloodFill(self.open_maze, (0, 0), (2, 2))
        self.assertTrue(solver.solve())
        self.assertEqual(solver.distances[0][0], len(solver.path) - 1)

    def _path_is_valid(self, maze: Maze, path: list[tuple[int, int]]) -> bool:
        if not path:
            return False

        for current, nxt in zip(path, path[1:]):
            if nxt not in maze.get_neighbors(*current):
                return False

        return True


if __name__ == "__main__":
    unittest.main()