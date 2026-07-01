"""Predefined mazes for quick demos and testing."""

from __future__ import annotations

from typing import Dict

from src.core.maze import Maze

from .maze_generator import generate_perfect_maze

_PRESET_CONFIGS: dict[str, tuple[int, int, int]] = {
    "tiny_5x5": (5, 5, 5),
    "small_8x8": (8, 8, 8),
    "medium_10x10": (10, 10, 10),
    "large_12x12": (12, 12, 12),
    "demo_15x15": (15, 15, 15),
}


def list_preset_names() -> list[str]:
    """Return the available preset names."""

    return list(_PRESET_CONFIGS)


def get_preset_maze(name: str) -> Maze:
    """Build a preset maze by name."""

    if name not in _PRESET_CONFIGS:
        raise KeyError(f"Unknown preset maze: {name}")

    rows, cols, seed = _PRESET_CONFIGS[name]
    return generate_perfect_maze(rows, cols, seed=seed)


def build_all_presets() -> Dict[str, Maze]:
    """Create all preset mazes as fresh Maze instances."""

    return {name: get_preset_maze(name) for name in _PRESET_CONFIGS}