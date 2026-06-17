# Maze-Solving-Technique

This project explores three classic maze-solving techniques, each with a distinct strategy:

- **Breadth-First Search (BFS):** Expands level by level from the start, so the first time it reaches the goal, the path is guaranteed to be the shortest in an unweighted maze.
- **Depth-First Search (DFS):** Dives deep along one route before backtracking, making it memory-efficient and useful for exploring all possible paths.
- **Flood Fill:** Spreads like “ink” through connected cells, marking reachable areas and helping visualize how regions of the maze are connected.

An interesting contrast is that BFS is usually best for shortest-path accuracy, DFS often finds a path faster in practice on narrow mazes, and Flood Fill is especially intuitive for visual analysis and region detection.