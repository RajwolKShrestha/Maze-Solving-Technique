# Viva Notes

## What to Explain Clearly

1. Why the wall bitmask representation is efficient.
2. Why BFS gives the shortest path in an unweighted maze.
3. Why DFS does not guarantee the shortest path.
4. How Dijkstra and A* improve on BFS.
5. How Flood Fill works in Micromouse solving.
6. Why the codebase is split into core, algorithms, visualization, editor, and utils.

## Short Answers

### Why bitmask walls?
They compress four wall states into one integer and allow fast `AND` checks.

### Why use a queue in BFS?
It explores cells in layers, which guarantees shortest-path discovery on unweighted grids.

### Why use a heuristic in A*?
The heuristic guides the search toward the goal so fewer nodes are expanded.

### Why is Flood Fill important?
It is a common Micromouse technique because it creates a distance map that can be followed locally.

### Why keep rendering separate from algorithms?
It keeps the logic testable and prevents the solver code from becoming tied to the UI.

## Suggested Demo Flow

1. Show a preset maze.
2. Run BFS and explain the path.
3. Switch to DFS and compare behavior.
4. Show A* or Dijkstra for a shortest-path variant.
5. Use Flood Fill and point out the distance heatmap.
6. End by showing the custom maze editor and save/load support.