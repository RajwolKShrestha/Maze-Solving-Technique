"""Simple performance benchmarking helpers for maze solvers."""

from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter

from src.algorithms import AStar, BFS, DFS, Dijkstra, FloodFill
from src.core.maze import Maze


@dataclass(frozen=True)
class BenchmarkResult:
    """Performance summary for one solver."""

    name: str
    solved: bool
    elapsed_ms: float
    steps: int
    path_length: int
    explored_count: int


DEFAULT_SOLVERS = {
    "BFS": BFS,
    "DFS": DFS,
    "Dijkstra": Dijkstra,
    "A*": AStar,
    "Flood Fill": FloodFill,
}


def benchmark_solvers(
    maze: Maze,
    start: tuple[int, int],
    goal: tuple[int, int],
    solver_classes: dict[str, type] | None = None,
) -> dict[str, BenchmarkResult]:
    """Run solvers once and capture timing plus search statistics."""

    solver_classes = solver_classes or DEFAULT_SOLVERS
    results: dict[str, BenchmarkResult] = {}

    for name, solver_class in solver_classes.items():
        solver = solver_class(maze, start, goal)
        started = perf_counter()
        solved = solver.solve()
        elapsed_ms = (perf_counter() - started) * 1000

        results[name] = BenchmarkResult(
            name=name,
            solved=solved,
            elapsed_ms=elapsed_ms,
            steps=solver.steps,
            path_length=len(solver.path),
            explored_count=len(solver.explored),
        )

    return results


def format_benchmark_results(results: dict[str, BenchmarkResult]) -> str:
    """Create a readable benchmark table."""

    lines = ["Algorithm | Solved | Time (ms) | Steps | Path | Explored", "---|---|---:|---:|---:|---:"]
    for result in results.values():
        lines.append(
            f"{result.name} | {result.solved} | {result.elapsed_ms:.2f} | {result.steps} | {result.path_length} | {result.explored_count}"
        )
    return "\n".join(lines)