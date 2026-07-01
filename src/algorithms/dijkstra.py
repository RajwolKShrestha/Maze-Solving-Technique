"""Dijkstra shortest-path solver for weighted or unweighted mazes."""

from __future__ import annotations

from heapq import heappop, heappush

from .base import SolverBase


class Dijkstra(SolverBase):
    """Compute the shortest path using Dijkstra's algorithm."""

    name = "Dijkstra"

    def get_time_complexity(self) -> str:
        return "O((V + E) log V)"

    def solve(self) -> bool:
        distances: dict[tuple[int, int], int] = {self.start: 0}
        parents: dict[tuple[int, int], tuple[int, int] | None] = {self.start: None}
        frontier: list[tuple[int, tuple[int, int]]] = [(0, self.start)]
        visited: set[tuple[int, int]] = set()

        while frontier:
            current_distance, current = heappop(frontier)
            if current in visited:
                continue

            visited.add(current)
            self.explored.append(current)
            self.steps += 1

            if current == self.goal:
                self.path = self._reconstruct_path(parents, current)
                return True

            for neighbor in self._neighbors(current):
                tentative_distance = current_distance + 1
                if tentative_distance < distances.get(neighbor, float("inf")):
                    distances[neighbor] = tentative_distance
                    parents[neighbor] = current
                    heappush(frontier, (tentative_distance, neighbor))

        self.path = []
        return False