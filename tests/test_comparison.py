"""Tests for algorithm comparison utilities."""

from __future__ import annotations

import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.algorithms import AStar, BFS, DFS, Dijkstra, FloodFill
from src.generators.maze_generator import generate_perfect_maze
from src.visualization.comparison import rank_by_path_then_steps, run_comparison


class TestComparisonUtilities(unittest.TestCase):
    def test_run_comparison_returns_all_algorithms(self) -> None:
        maze = generate_perfect_maze(5, 5, seed=4)
        snapshots = run_comparison(
            maze,
            (0, 0),
            (4, 4),
            {
                "BFS": BFS,
                "DFS": DFS,
                "Dijkstra": Dijkstra,
                "A*": AStar,
                "Flood Fill": FloodFill,
            },
        )

        self.assertEqual(set(snapshots.keys()), {"BFS", "DFS", "Dijkstra", "A*", "Flood Fill"})
        self.assertTrue(all(snapshot.solved for snapshot in snapshots.values()))

    def test_ranking_orders_by_path_then_steps(self) -> None:
        maze = generate_perfect_maze(5, 5, seed=4)
        snapshots = run_comparison(
            maze,
            (0, 0),
            (4, 4),
            {
                "BFS": BFS,
                "DFS": DFS,
                "Dijkstra": Dijkstra,
                "A*": AStar,
                "Flood Fill": FloodFill,
            },
        )

        ranked = rank_by_path_then_steps(snapshots)
        self.assertGreaterEqual(len(ranked), 1)
        self.assertEqual(ranked[0].path_length, min(snapshot.path_length for snapshot in snapshots.values()))


if __name__ == "__main__":
    unittest.main()