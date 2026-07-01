"""Helpers for comparing maze-solving algorithms side by side."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from src.core.maze import Maze


@dataclass(frozen=True)
class AlgorithmSnapshot:
    """Result summary for one solver execution."""

    name: str
    solved: bool
    steps: int
    path_length: int
    explored_count: int
    elapsed_ms: float


def run_comparison(
    maze: Maze,
    start: tuple[int, int],
    goal: tuple[int, int],
    algorithm_classes: dict[str, type],
) -> dict[str, AlgorithmSnapshot]:
    """Run each algorithm once and capture a compact summary."""

    snapshots: dict[str, AlgorithmSnapshot] = {}

    for name, algorithm_class in algorithm_classes.items():
        solver = algorithm_class(maze, start, goal)
        start_time = perf_counter()
        solved = solver.solve()
        elapsed_ms = (perf_counter() - start_time) * 1000

        snapshots[name] = AlgorithmSnapshot(
            name=name,
            solved=solved,
            steps=solver.steps,
            path_length=len(solver.path),
            explored_count=len(solver.explored),
            elapsed_ms=elapsed_ms,
        )

    return snapshots


def rank_by_path_then_steps(snapshots: dict[str, AlgorithmSnapshot]) -> list[AlgorithmSnapshot]:
    """Return a stable ranking of solved algorithms."""

    return sorted(
        (snapshot for snapshot in snapshots.values() if snapshot.solved),
        key=lambda snapshot: (snapshot.path_length, snapshot.steps, snapshot.elapsed_ms),
    )