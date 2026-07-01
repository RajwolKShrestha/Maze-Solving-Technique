# Data Structure Guide

## Wall Bitmask Grid

Each maze cell stores a 4-bit integer:

- `8` = North wall
- `4` = South wall
- `2` = East wall
- `1` = West wall

Example:

- `0b1010` means North and East walls are present.

Why it matters:

- A single integer keeps the model compact.
- Bitwise checks are fast and easy to explain.
- The format mirrors embedded robotics practice.

## Visited Cells

Visited states are tracked with a `set` or list depending on the algorithm.

- `set` is used for constant-time membership tests.
- `list` preserves exploration order for visualization.

## Paths

Paths are stored as ordered `(row, col)` coordinates.

- The path begins at the start cell.
- The path ends at the goal cell.
- It can be drawn directly on the renderer without extra conversion.

## Flood Fill Distance Map

The flood fill solver stores a 2D distance matrix.

- The goal starts at distance `0`.
- Each reachable cell gets the number of steps to the goal.
- The mouse follows the steepest distance drop.

## File Format

Maze files are stored as plain text:

1. first line = `rows,cols`
2. following lines = comma-separated wall bitmasks

This format is easy to inspect, edit, and debug.