# Architecture Overview

This project is organized around a small set of focused modules so the maze logic, algorithms, visualization, and editing tools stay independent.

## Core Layers

### `src/core/`
Contains the maze model and shared constants.

- `maze.py` stores the wall bitmask grid.
- `constants.py` defines directions, colors, and grid defaults.

### `src/generators/`
Builds reusable mazes.

- `maze_generator.py` creates randomized perfect mazes.
- `presets.py` exposes stable demo mazes.

### `src/algorithms/`
Contains the solvers.

- `bfs.py` and `dfs.py` provide the baseline traversals.
- `dijkstra.py`, `astar.py`, and `flood_fill.py` add shortest-path and Micromouse-style solving.

### `src/visualization/`
Draws the maze and solver state.

- `renderer.py` handles walls, paths, visited cells, heatmaps, and bitmask overlays.
- `animator.py` manages playback state.
- `ui_elements.py` and comparison modules provide interactive controls and result panels.

### `src/editor/`
Supports interactive maze editing and persistence.

### `src/utils/`
Provides file handling and benchmark helpers.

## Design Rules

1. The maze model does not know about Pygame.
2. Algorithms read the maze and produce exploration state.
3. Visualization reads solver output and draws it.
4. File I/O is separate from editing logic.

This keeps the system testable and makes each project layer easy to explain in a viva.