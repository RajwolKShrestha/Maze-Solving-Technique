"""Breadth-first search maze solver."""

from __future__ import annotations

from collections import deque

from .base import SolverBase


class BFS(SolverBase):
    """Find the shortest path in an unweighted maze."""

    name = "BFS"

    def solve(self) -> bool:
        queue = deque([self.start])
        parents: dict[tuple[int, int], tuple[int, int] | None] = {self.start: None}
        visited = {self.start}

        while queue:
            current = queue.popleft()
            self.explored.append(current)
            self.steps += 1

            if current == self.goal:
                self.path = self._reconstruct_path(parents, current)
                return True

            for neighbor in self._neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    parents[neighbor] = current
                    queue.append(neighbor)

        self.path = []
        return False