"""Flood Fill solver for Micromouse-style navigation."""

from __future__ import annotations

from collections import deque

from .base import SolverBase


class FloodFill(SolverBase):
    """Compute a distance field from the goal, then follow the gradient."""

    name = "Flood Fill"

    def get_time_complexity(self) -> str:
        return "O(V + E)"

    def solve(self) -> bool:
        rows, cols = self.maze.rows, self.maze.cols
        self.distances = [[float("inf") for _ in range(cols)] for _ in range(rows)]
        goal_row, goal_col = self.goal
        self.distances[goal_row][goal_col] = 0

        queue = deque([self.goal])
        explored_order: list[tuple[int, int]] = []

        while queue:
            current = queue.popleft()
            explored_order.append(current)
            self.steps += 1

            current_distance = self.distances[current[0]][current[1]]
            for neighbor in self._neighbors(current):
                next_row, next_col = neighbor
                if current_distance + 1 < self.distances[next_row][next_col]:
                    self.distances[next_row][next_col] = current_distance + 1
                    queue.append(neighbor)

        self.explored = explored_order

        if self.distances[self.start[0]][self.start[1]] == float("inf"):
            self.path = []
            return False

        path = [self.start]
        current = self.start

        while current != self.goal:
            neighbors = self._neighbors(current)
            next_cell = min(
                neighbors,
                key=lambda cell: self.distances[cell[0]][cell[1]],
                default=None,
            )

            if next_cell is None or self.distances[next_cell[0]][next_cell[1]] >= self.distances[current[0]][current[1]]:
                self.path = []
                return False

            path.append(next_cell)
            current = next_cell

        self.path = path
        return True