"""
Unit tests for the Maze class
Testing bitmask wall storage, validation, and connectivity
"""

import unittest
import sys
from pathlib import Path

# Add src directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.maze import Maze
from src.core.constants import NORTH, SOUTH, EAST, WEST


class TestMazeInitialization(unittest.TestCase):
    """Test maze initialization"""
    
    def test_maze_creation_with_all_walls(self):
        """Test creating a maze with all walls"""
        maze = Maze(5, 5, all_walls=True)
        self.assertEqual(maze.rows, 5)
        self.assertEqual(maze.cols, 5)
        
        # Check that all cells have all walls
        for row in range(5):
            for col in range(5):
                for direction in [NORTH, SOUTH, EAST, WEST]:
                    self.assertTrue(maze.has_wall(row, col, direction))
    
    def test_maze_creation_without_walls(self):
        """Test creating a maze with no walls"""
        maze = Maze(5, 5, all_walls=False)
        self.assertEqual(maze.rows, 5)
        self.assertEqual(maze.cols, 5)
        
        # Check that all cells have no walls
        for row in range(5):
            for col in range(5):
                for direction in [NORTH, SOUTH, EAST, WEST]:
                    self.assertFalse(maze.has_wall(row, col, direction))
    
    def test_different_dimensions(self):
        """Test maze with different dimensions"""
        maze1 = Maze(10, 10)
        self.assertEqual(maze1.rows, 10)
        self.assertEqual(maze1.cols, 10)
        
        maze2 = Maze(3, 7)
        self.assertEqual(maze2.rows, 3)
        self.assertEqual(maze2.cols, 7)


class TestWallOperations(unittest.TestCase):
    """Test wall addition and removal"""
    
    def setUp(self):
        """Create a fresh maze for each test"""
        self.maze = Maze(5, 5, all_walls=False)
    
    def test_add_wall(self):
        """Test adding a wall"""
        self.assertFalse(self.maze.has_wall(0, 0, NORTH))
        self.maze.add_wall(0, 0, NORTH)
        self.assertTrue(self.maze.has_wall(0, 0, NORTH))
    
    def test_remove_wall(self):
        """Test removing a wall"""
        maze = Maze(5, 5, all_walls=True)
        self.assertTrue(maze.has_wall(0, 0, NORTH))
        maze.remove_wall(0, 0, NORTH)
        self.assertFalse(maze.has_wall(0, 0, NORTH))
    
    def test_multiple_walls(self):
        """Test adding multiple walls to a cell"""
        self.maze.add_wall(2, 2, NORTH)
        self.maze.add_wall(2, 2, EAST)
        self.maze.add_wall(2, 2, SOUTH)
        
        self.assertTrue(self.maze.has_wall(2, 2, NORTH))
        self.assertTrue(self.maze.has_wall(2, 2, EAST))
        self.assertTrue(self.maze.has_wall(2, 2, SOUTH))
        self.assertFalse(self.maze.has_wall(2, 2, WEST))
    
    def test_wall_state(self):
        """Test getting wall state"""
        self.maze.add_wall(1, 1, NORTH)
        self.maze.add_wall(1, 1, WEST)
        
        wall_state = self.maze.get_wall_state(1, 1)
        # NORTH (8) + WEST (1) = 9
        self.assertEqual(wall_state, 9)


class TestCellValidation(unittest.TestCase):
    """Test cell validation"""
    
    def setUp(self):
        self.maze = Maze(5, 5)
    
    def test_valid_cell(self):
        """Test valid cell coordinates"""
        self.assertTrue(self.maze.is_valid_cell(0, 0))
        self.assertTrue(self.maze.is_valid_cell(2, 2))
        self.assertTrue(self.maze.is_valid_cell(4, 4))
    
    def test_invalid_cell(self):
        """Test invalid cell coordinates"""
        self.assertFalse(self.maze.is_valid_cell(-1, 0))
        self.assertFalse(self.maze.is_valid_cell(0, -1))
        self.assertFalse(self.maze.is_valid_cell(5, 5))
        self.assertFalse(self.maze.is_valid_cell(0, 5))
    
    def test_out_of_bounds_error(self):
        """Test error on out of bounds access"""
        with self.assertRaises(ValueError):
            self.maze.has_wall(-1, 0, NORTH)
        
        with self.assertRaises(ValueError):
            self.maze.has_wall(5, 5, NORTH)


class TestCellConnectivity(unittest.TestCase):
    """Test connecting cells (removing walls between them)"""
    
    def setUp(self):
        self.maze = Maze(5, 5, all_walls=True)
    
    def test_connect_adjacent_cells_north_south(self):
        """Test connecting cells vertically"""
        self.assertTrue(self.maze.connect_cells(1, 1, 2, 1))
        
        # Check walls were removed from both sides
        self.assertFalse(self.maze.has_wall(1, 1, SOUTH))
        self.assertFalse(self.maze.has_wall(2, 1, NORTH))
        
        # Check other walls remain
        self.assertTrue(self.maze.has_wall(1, 1, NORTH))
        self.assertTrue(self.maze.has_wall(2, 1, SOUTH))
    
    def test_connect_adjacent_cells_east_west(self):
        """Test connecting cells horizontally"""
        self.assertTrue(self.maze.connect_cells(1, 1, 1, 2))
        
        # Check walls were removed from both sides
        self.assertFalse(self.maze.has_wall(1, 1, EAST))
        self.assertFalse(self.maze.has_wall(1, 2, WEST))
    
    def test_connect_non_adjacent_cells(self):
        """Test that non-adjacent cells cannot be connected"""
        result = self.maze.connect_cells(0, 0, 2, 2)
        self.assertFalse(result)
    
    def test_bidirectional_connection(self):
        """Test that connections are bidirectional"""
        self.maze.connect_cells(0, 0, 1, 0)
        
        # Check from both directions
        neighbors_from_00 = self.maze.get_neighbors(0, 0)
        neighbors_from_10 = self.maze.get_neighbors(1, 0)
        
        self.assertIn((1, 0), neighbors_from_00)
        self.assertIn((0, 0), neighbors_from_10)


class TestNeighbors(unittest.TestCase):
    """Test getting accessible neighbors"""
    
    def setUp(self):
        self.maze = Maze(5, 5, all_walls=True)
    
    def test_no_neighbors_isolated_cell(self):
        """Test cell with all walls has no neighbors"""
        neighbors = self.maze.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 0)
    
    def test_single_neighbor(self):
        """Test cell with one neighbor"""
        self.maze.connect_cells(2, 2, 2, 3)
        neighbors = self.maze.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 1)
        self.assertIn((2, 3), neighbors)
    
    def test_multiple_neighbors(self):
        """Test cell with multiple neighbors"""
        self.maze.connect_cells(2, 2, 2, 3)  # East
        self.maze.connect_cells(2, 2, 3, 2)  # South
        self.maze.connect_cells(2, 2, 1, 2)  # North
        
        neighbors = self.maze.get_neighbors(2, 2)
        self.assertEqual(len(neighbors), 3)
        self.assertIn((2, 3), neighbors)
        self.assertIn((3, 2), neighbors)
        self.assertIn((1, 2), neighbors)
    
    def test_boundary_neighbors(self):
        """Test getting neighbors at maze boundary"""
        self.maze = Maze(3, 3, all_walls=True)
        
        # Connect corner cell (0,0) to neighbors
        self.maze.connect_cells(0, 0, 1, 0)
        self.maze.connect_cells(0, 0, 0, 1)
        
        neighbors = self.maze.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 2)


class TestMazeValidation(unittest.TestCase):
    """Test maze validation"""
    
    def test_valid_maze_all_walls(self):
        """Test that new maze with all walls is valid"""
        maze = Maze(5, 5, all_walls=True)
        self.assertTrue(maze.validate_maze())
    
    def test_valid_maze_no_walls(self):
        """Test that maze with no walls is valid"""
        maze = Maze(5, 5, all_walls=False)
        self.assertTrue(maze.validate_maze())
    
    def test_valid_maze_after_connection(self):
        """Test that maze is valid after connecting cells"""
        maze = Maze(5, 5, all_walls=True)
        maze.connect_cells(0, 0, 1, 0)
        maze.connect_cells(1, 0, 1, 1)
        self.assertTrue(maze.validate_maze())
    
    def test_invalid_maze_inconsistent_walls(self):
        """Test detection of inconsistent walls"""
        maze = Maze(5, 5, all_walls=True)
        
        # Manually create inconsistent state (remove wall from only one side)
        maze.remove_wall(2, 2, SOUTH)
        # Note: NOT removing wall from (3,2) NORTH side
        
        self.assertFalse(maze.validate_maze())


class TestWallCounting(unittest.TestCase):
    """Test wall counting"""
    
    def test_count_walls_all_walls(self):
        """Test counting all walls"""
        maze = Maze(3, 3, all_walls=True)
        # 3x3 grid has perimeter walls and internal walls
        # Total = 3*3*4 = 36 wall instances (some are duplicates at boundaries)
        # Actually count: 32 (interior walls don't have all 4 directions)
        wall_count = maze.count_walls()
        self.assertGreater(wall_count, 0)
    
    def test_count_walls_no_walls(self):
        """Test counting with no walls"""
        maze = Maze(3, 3, all_walls=False)
        wall_count = maze.count_walls()
        self.assertEqual(wall_count, 0)
    
    def test_count_walls_after_removal(self):
        """Test counting after removing walls"""
        maze = Maze(5, 5, all_walls=True)
        initial_count = maze.count_walls()
        
        maze.connect_cells(2, 2, 2, 3)
        final_count = maze.count_walls()
        
        # Should have removed 2 walls
        self.assertEqual(initial_count - final_count, 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases"""
    
    def test_1x1_maze(self):
        """Test minimal 1x1 maze"""
        maze = Maze(1, 1)
        self.assertEqual(maze.rows, 1)
        self.assertEqual(maze.cols, 1)
        
        neighbors = maze.get_neighbors(0, 0)
        self.assertEqual(len(neighbors), 0)
    
    def test_large_maze(self):
        """Test large maze"""
        maze = Maze(100, 100)
        self.assertEqual(maze.rows, 100)
        self.assertEqual(maze.cols, 100)
        self.assertTrue(maze.validate_maze())


if __name__ == '__main__':
    unittest.main()
