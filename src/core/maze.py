"""
Maze class using bitmask wall storage system
Efficient representation of maze walls for DSA algorithms
"""

from .constants import NORTH, SOUTH, EAST, WEST, OPPOSITE_DIRECTION, DIRECTION_MAP, DIRECTIONS


class Maze:
    """
    Represents a maze using a 2D grid with bitmask wall representation.
    
    Each cell stores a 4-bit integer representing walls in 4 directions:
    - Bit 3 (NORTH): Wall to North
    - Bit 2 (SOUTH): Wall to South
    - Bit 1 (EAST): Wall to East
    - Bit 0 (WEST): Wall to West
    
    Example:
        maze = Maze(10, 10)  # Create 10x10 maze
        maze.add_wall(0, 0, NORTH)  # Add wall to north of cell (0,0)
        maze.remove_wall(0, 0, NORTH)  # Remove that wall
    """
    
    def __init__(self, rows: int, cols: int, all_walls: bool = True):
        """
        Initialize a maze with given dimensions.
        
        Args:
            rows (int): Number of rows in the maze
            cols (int): Number of columns in the maze
            all_walls (bool): If True, start with all walls present (default True)
        """
        self.rows = rows
        self.cols = cols
        
        # Initialize wall matrix
        if all_walls:
            # Start with all walls (15 = 0b1111)
            initial_value = NORTH | SOUTH | EAST | WEST
        else:
            # Start with no walls (0 = 0b0000)
            initial_value = 0
        
        self.walls = [[initial_value for _ in range(cols)] for _ in range(rows)]
    
    def is_valid_cell(self, row: int, col: int) -> bool:
        """
        Check if a cell is within maze bounds.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            bool: True if cell is valid, False otherwise
        """
        return 0 <= row < self.rows and 0 <= col < self.cols
    
    def has_wall(self, row: int, col: int, direction: int) -> bool:
        """
        Check if there is a wall in the specified direction from a cell.
        
        Args:
            row (int): Row index of the cell
            col (int): Column index of the cell
            direction (int): Direction constant (NORTH, SOUTH, EAST, WEST)
            
        Returns:
            bool: True if wall exists, False otherwise
            
        Raises:
            ValueError: If cell is out of bounds or direction is invalid
        """
        if not self.is_valid_cell(row, col):
            raise ValueError(f"Cell ({row}, {col}) is out of bounds")
        
        if direction not in [NORTH, SOUTH, EAST, WEST]:
            raise ValueError(f"Invalid direction: {direction}")
        
        return (self.walls[row][col] & direction) != 0
    
    def add_wall(self, row: int, col: int, direction: int) -> None:
        """
        Add a wall in the specified direction from a cell.
        
        Args:
            row (int): Row index of the cell
            col (int): Column index of the cell
            direction (int): Direction constant (NORTH, SOUTH, EAST, WEST)
            
        Raises:
            ValueError: If cell is out of bounds or direction is invalid
        """
        if not self.is_valid_cell(row, col):
            raise ValueError(f"Cell ({row}, {col}) is out of bounds")
        
        if direction not in [NORTH, SOUTH, EAST, WEST]:
            raise ValueError(f"Invalid direction: {direction}")
        
        self.walls[row][col] |= direction
    
    def remove_wall(self, row: int, col: int, direction: int) -> None:
        """
        Remove a wall in the specified direction from a cell.
        
        Args:
            row (int): Row index of the cell
            col (int): Column index of the cell
            direction (int): Direction constant (NORTH, SOUTH, EAST, WEST)
            
        Raises:
            ValueError: If cell is out of bounds or direction is invalid
        """
        if not self.is_valid_cell(row, col):
            raise ValueError(f"Cell ({row}, {col}) is out of bounds")
        
        if direction not in [NORTH, SOUTH, EAST, WEST]:
            raise ValueError(f"Invalid direction: {direction}")
        
        self.walls[row][col] &= ~direction
    
    def connect_cells(self, row1: int, col1: int, row2: int, col2: int) -> bool:
        """
        Create a passage between two adjacent cells by removing walls between them.
        
        Args:
            row1 (int): Row of first cell
            col1 (int): Column of first cell
            row2 (int): Row of second cell
            col2 (int): Column of second cell
            
        Returns:
            bool: True if cells were successfully connected, False if not adjacent
        """
        if abs(row1 - row2) + abs(col1 - col2) != 1:
            return False  # Cells not adjacent
        
        # Determine direction from cell1 to cell2
        if row2 < row1:
            direction = NORTH
        elif row2 > row1:
            direction = SOUTH
        elif col2 < col1:
            direction = WEST
        else:
            direction = EAST
        
        # Remove wall in both directions
        self.remove_wall(row1, col1, direction)
        opposite = OPPOSITE_DIRECTION[direction]
        self.remove_wall(row2, col2, opposite)
        
        return True
    
    def get_wall_state(self, row: int, col: int) -> int:
        """
        Get the wall state of a cell as a bitmask.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            int: 4-bit integer representing walls (0-15)
        """
        if not self.is_valid_cell(row, col):
            raise ValueError(f"Cell ({row}, {col}) is out of bounds")
        
        return self.walls[row][col]
    
    def get_wall_state_binary(self, row: int, col: int) -> str:
        """
        Get the wall state as a binary string for debugging.
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            str: Binary representation (e.g., '0b1010')
        """
        return bin(self.get_wall_state(row, col))
    
    def get_neighbors(self, row: int, col: int) -> list:
        """
        Get all passable neighbors of a cell (no wall between them).
        
        Args:
            row (int): Row index
            col (int): Column index
            
        Returns:
            list: List of (row, col) tuples of accessible neighbors
        """
        neighbors = []
        
        for direction in DIRECTIONS:
            if not self.has_wall(row, col, direction):
                delta_row, delta_col = DIRECTION_MAP[direction]
                new_row, new_col = row + delta_row, col + delta_col
                
                if self.is_valid_cell(new_row, new_col):
                    neighbors.append((new_row, new_col))
        
        return neighbors
    
    def count_walls(self) -> int:
        """
        Count the total number of walls in the maze.
        
        Returns:
            int: Total wall count
        """
        wall_count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                for direction in DIRECTIONS:
                    if self.has_wall(row, col, direction):
                        wall_count += 1
        return wall_count
    
    def validate_maze(self) -> bool:
        """
        Validate that maze walls are consistent (bidirectional).
        A wall between two cells must exist on both sides.
        
        Returns:
            bool: True if maze is valid, False otherwise
        """
        for row in range(self.rows):
            for col in range(self.cols):
                for direction in DIRECTIONS:
                    if self.has_wall(row, col, direction):
                        # Check if neighbor exists and has opposite wall
                        delta_row, delta_col = DIRECTION_MAP[direction]
                        neighbor_row = row + delta_row
                        neighbor_col = col + delta_col
                        
                        if self.is_valid_cell(neighbor_row, neighbor_col):
                            opposite = OPPOSITE_DIRECTION[direction]
                            if not self.has_wall(neighbor_row, neighbor_col, opposite):
                                return False
        
        return True
    
    def __repr__(self) -> str:
        """Return string representation of the maze."""
        return f"Maze({self.rows}x{self.cols})"
