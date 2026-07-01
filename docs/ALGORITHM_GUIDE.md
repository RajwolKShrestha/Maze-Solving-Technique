# Algorithm Guide

## BFS

- Purpose: shortest path in an unweighted grid.
- Data structure: queue.
- Time complexity: `O(V + E)`.
- Strength: guarantees the shortest path.

## DFS

- Purpose: deep exploration and backtracking.
- Data structure: stack.
- Time complexity: `O(V + E)`.
- Strength: simple and memory-light.

## Dijkstra

- Purpose: shortest path with weighted movement support.
- Data structure: priority queue.
- Time complexity: `O((V + E) log V)`.
- Strength: robust and widely applicable.

## A*

- Purpose: shortest path with heuristic guidance.
- Data structure: priority queue.
- Heuristic used: Manhattan distance.
- Time complexity: `O((V + E) log V)`.
- Strength: usually faster than Dijkstra on grids.

## Flood Fill

- Purpose: Micromouse-style distance map solving.
- Data structure: queue plus distance field.
- Time complexity: `O(V + E)`.
- Strength: ideal for maze navigation and real-time distance updates.

## Comparison Notes

- BFS and Flood Fill are the strongest choices for demonstrating grid logic clearly.
- DFS is useful for exploration but not for shortest-path guarantees.
- Dijkstra and A* demonstrate the transition from basic graph search to informed search.