"""A* maze solver using the Manhattan distance heuristic."""

from __future__ import annotations

from heapq import heappop, heappush

from .base import SolverBase


class AStar(SolverBase):
    """Find a shortest path using A* search."""

    name = "A*"

    def get_time_complexity(self) -> str:
        return "O((V + E) log V)"

    def _heuristic(self, cell: tuple[int, int]) -> int:
        return abs(cell[0] - self.goal[0]) + abs(cell[1] - self.goal[1])

    def solve(self) -> bool:
        g_costs: dict[tuple[int, int], int] = {self.start: 0}
        parents: dict[tuple[int, int], tuple[int, int] | None] = {self.start: None}
        frontier: list[tuple[int, int, tuple[int, int]]] = [(self._heuristic(self.start), 0, self.start)]
        visited: set[tuple[int, int]] = set()

        while frontier:
            _, current_cost, current = heappop(frontier)
            if current in visited:
                continue

            visited.add(current)
            self.explored.append(current)
            self.steps += 1

            if current == self.goal:
                self.path = self._reconstruct_path(parents, current)
                return True

            for neighbor in self._neighbors(current):
                tentative_cost = current_cost + 1
                if tentative_cost < g_costs.get(neighbor, float("inf")):
                    g_costs[neighbor] = tentative_cost
                    parents[neighbor] = current
                    priority = tentative_cost + self._heuristic(neighbor)
                    heappush(frontier, (priority, tentative_cost, neighbor))

        self.path = []
        return False