# Global Simulation Settings

# Map Dimensions
GRID_WIDTH = 100
GRID_HEIGHT = 100
CELL_SIZE = 1.0  # meters

# Time Settings
TIME_STEP = 0.1  # seconds per frame
MAX_STEPS = 1000

# Agent Settings
DEFAULT_SPEED = 1.5  # m/s
PANIC_SPEED_FACTOR = 1.5
REACTION_TIME_MEAN = 0.5  # seconds
VISUAL_RANGE = 10  # meters

# Panic Settings
PANIC_INFECTION_RATE = 0.1
PANIC_DECAY = 0.01

# Colors for Visualization
COLOR_WALL = '#000000'
COLOR_EXIT = '#00FF00'
COLOR_AGENT_NORMAL = '#0000FF'
COLOR_AGENT_PANIC = '#FF0000'
