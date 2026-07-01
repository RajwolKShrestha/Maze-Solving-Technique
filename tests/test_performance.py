"""Tests for benchmark helper output."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.maze import Maze
from src.utils.performance import benchmark_solvers, format_benchmark_results


class TestPerformanceHelpers(unittest.TestCase):
    def test_benchmark_solvers_returns_all_default_algorithms(self) -> None:
        maze = Maze(4, 4, all_walls=False)
        results = benchmark_solvers(maze, (0, 0), (3, 3))

        self.assertEqual(set(results.keys()), {"BFS", "DFS", "Dijkstra", "A*", "Flood Fill"})
        self.assertTrue(all(result.elapsed_ms >= 0 for result in results.values()))

    def test_format_benchmark_results_contains_table_header(self) -> None:
        maze = Maze(4, 4, all_walls=False)
        results = benchmark_solvers(maze, (0, 0), (3, 3))
        table = format_benchmark_results(results)

        self.assertIn("Algorithm | Solved | Time (ms)", table)
        self.assertIn("BFS", table)


if __name__ == "__main__":
    unittest.main()