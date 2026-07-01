"""Shared solver utilities for maze-search algorithms."""

from __future__ import annotations

from collections import deque
from typing import Deque, Iterable

from src.core.maze import Maze


class SolverBase:
    """Base class for maze solvers.

    Subclasses are expected to implement `solve()` and populate `path`,
    `explored`, and `steps`.
    """

    name = "BaseSolver"

    def __init__(self, maze: Maze, start: tuple[int, int], goal: tuple[int, int]):
        self.maze = maze
        self.start = start
        self.goal = goal
        self.path: list[tuple[int, int]] = []
        self.explored: list[tuple[int, int]] = []
        self.steps = 0

    def solve(self) -> bool:
        raise NotImplementedError

    def get_time_complexity(self) -> str:
        return "O(V + E)"

    def get_metrics(self) -> dict[str, int | str]:
        return {
            "algorithm": self.name,
            "steps": self.steps,
            "path_length": len(self.path),
            "cells_explored": len(self.explored),
            "time_complexity": self.get_time_complexity(),
        }

    def _reconstruct_path(
        self,
        parents: dict[tuple[int, int], tuple[int, int] | None],
        end: tuple[int, int],
    ) -> list[tuple[int, int]]:
        path: list[tuple[int, int]] = []
        current: tuple[int, int] | None = end

        while current is not None:
            path.append(current)
            current = parents[current]

        path.reverse()
        return path

    def _neighbors(self, cell: tuple[int, int]) -> list[tuple[int, int]]:
        row, col = cell
        return self.maze.get_neighbors(row, col)