"""
Core module containing fundamental data structures and utilities
"""

from .maze import Maze
from .constants import (
    NORTH, SOUTH, EAST, WEST,
    DIRECTIONS, ROWS, COLS,
    COLORS
)

__all__ = ['Maze', 'NORTH', 'SOUTH', 'EAST', 'WEST', 'DIRECTIONS', 'ROWS', 'COLS', 'COLORS']
