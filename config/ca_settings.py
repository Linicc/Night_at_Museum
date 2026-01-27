"""CA-specific configuration settings."""

# Grid dimensions
GRID_WIDTH = 100
GRID_HEIGHT = 100

# Simulation parameters
MAX_TIMESTEPS = 1000
INITIAL_POPULATION = 75

# Behavior parameters
PANIC_SPREAD_RATE = 0.05
PANIC_DECAY_RATE = 0.01
CROWDING_THRESHOLD = 5

# Movement parameters
# 80% greedy (follow attractiveness), 20% random exploration
GREEDY_PROBABILITY = 0.80
RANDOM_MOVE_PROBABILITY = 0.20

# High panic threshold for changing movement strategy
HIGH_PANIC_THRESHOLD = 0.6

# Snapshot and output
SNAPSHOT_INTERVAL = 100  # Save grid snapshot every N steps
OUTPUT_DIR = "output"
CONFIG_FILE = "config/museum_ca_config.xlsx"

# Excel output settings
TIMESTEP_SNAPSHOT_SKIP = 100  # Save timestep sheets every 100 steps
