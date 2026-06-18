"""
Constants and configuration for the Maze Solving application
"""

# ============================================================================
# DIRECTION CONSTANTS (Bitmask System)
# ============================================================================
# Each direction is represented as a single bit for efficient wall storage
# Wall state is stored as a 4-bit value in each cell

NORTH = 0b1000  # 8 - Wall to the North (top)
SOUTH = 0b0100  # 4 - Wall to the South (bottom)
EAST  = 0b0010  # 2 - Wall to the East (right)
WEST  = 0b0001  # 1 - Wall to the West (left)

# Direction tuples: (row_delta, col_delta)
DIRECTION_MAP = {
    NORTH: (-1, 0),
    SOUTH: (1, 0),
    EAST: (0, 1),
    WEST: (0, -1),
}

DIRECTIONS = [NORTH, SOUTH, EAST, WEST]

# Opposite directions for wall removal
OPPOSITE_DIRECTION = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    EAST: WEST,
    WEST: EAST,
}

# Direction names for debugging
DIRECTION_NAMES = {
    NORTH: "NORTH",
    SOUTH: "SOUTH",
    EAST: "EAST",
    WEST: "WEST",
}

# ============================================================================
# GRID CONFIGURATION
# ============================================================================

ROWS = 10  # Default grid height
COLS = 10  # Default grid width

# ============================================================================
# COLOR SCHEME (RGB Tuples)
# ============================================================================

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'gray': (128, 128, 128),
    'light_gray': (200, 200, 200),
    'dark_gray': (64, 64, 64),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'blue': (0, 0, 255),
    'yellow': (255, 255, 0),
    'cyan': (0, 255, 255),
    'magenta': (255, 0, 255),
    'light_blue': (173, 216, 230),
    'dark_green': (0, 128, 0),
}

# Cell state colors
CELL_COLORS = {
    'wall': COLORS['black'],
    'path': COLORS['white'],
    'start': COLORS['green'],
    'end': COLORS['red'],
    'visited': COLORS['light_blue'],
    'solution': COLORS['yellow'],
    'current': COLORS['cyan'],
}
