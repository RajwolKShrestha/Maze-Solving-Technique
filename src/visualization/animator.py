"""Simple animation state helper for solver playback."""

from __future__ import annotations


class Animator:
    """Track playback progress through explored cells and final path."""

    def __init__(self, explored: list[tuple[int, int]], path: list[tuple[int, int]]):
        self.explored = explored
        self.path = path
        self.current_step = 0
        self.is_playing = False

    def reset(self) -> None:
        self.current_step = 0
        self.is_playing = False

    def step_forward(self) -> bool:
        if self.current_step < len(self.explored):
            self.current_step += 1
            return True
        return False

    def completed_explored(self) -> bool:
        return self.current_step >= len(self.explored)

    def visible_explored(self) -> list[tuple[int, int]]:
        return self.explored[: self.current_step]

    def visible_path(self) -> list[tuple[int, int]]:
        if self.completed_explored():
            return self.path
        return []