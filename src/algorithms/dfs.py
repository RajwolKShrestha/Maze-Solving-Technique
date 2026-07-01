"""Depth-first search maze solver."""

from __future__ import annotations

from .base import SolverBase


class DFS(SolverBase):
    """Explore a maze using a stack-based depth-first search."""

    name = "DFS"

    def solve(self) -> bool:
        stack = [self.start]
        parents: dict[tuple[int, int], tuple[int, int] | None] = {self.start: None}
        visited = set()

        while stack:
            current = stack.pop()
            if current in visited:
                continue

            visited.add(current)
            self.explored.append(current)
            self.steps += 1

            if current == self.goal:
                self.path = self._reconstruct_path(parents, current)
                return True

            neighbors = self._neighbors(current)
            for neighbor in reversed(neighbors):
                if neighbor not in visited and neighbor not in parents:
                    parents[neighbor] = current
                    stack.append(neighbor)

        self.path = []
        return False