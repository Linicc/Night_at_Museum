"""Dual-layer grid management for cellular automaton simulation."""
import numpy as np

# Cell type encodings
CELL_EMPTY = 0
CELL_PERSON = 1
CELL_WALL = 2
CELL_EXIT = 3
CELL_ENTRANCE = 4
CELL_EXHIBIT = 5
CELL_EXHIBIT_SPECIAL = 6
CELL_SECURITY = 7


class CAGrid:
    """Manages a dual-layer grid: static environment and dynamic agent positions."""

    def __init__(self, width, height):
        """Initialize grid with given dimensions."""
        self.width = width
        self.height = height

        # Static layer: environment features (walls, exits, exhibits) - doesn't change
        self.static_layer = np.zeros((width, height), dtype=np.uint8)

        # Dynamic layer: agent positions - updated each step
        self.dynamic_layer = np.zeros((width, height), dtype=np.uint8)

        # Track agent occupancy (multiple agents per cell possible in tracking)
        self.agent_positions = {}  # {agent_id: (x, y)}

    def is_walkable(self, x, y):
        """Check if cell is walkable (not a wall)."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.static_layer[x, y] != CELL_WALL

    def is_occupied(self, x, y):
        """Check if cell is occupied by an agent."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        return self.dynamic_layer[x, y] == CELL_PERSON

    def place_agent(self, agent_id, x, y):
        """Place agent at position. Returns success."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        if not self.is_walkable(x, y):
            return False

        # Update tracking
        if agent_id in self.agent_positions:
            old_x, old_y = self.agent_positions[agent_id]
            self.dynamic_layer[old_x, old_y] = CELL_EMPTY

        self.agent_positions[agent_id] = (x, y)
        self.dynamic_layer[x, y] = CELL_PERSON
        return True

    def move_agent(self, agent_id, new_x, new_y):
        """Move agent from current position to new position."""
        if agent_id not in self.agent_positions:
            return False
        if not self.is_walkable(new_x, new_y):
            return False

        old_x, old_y = self.agent_positions[agent_id]
        self.dynamic_layer[old_x, old_y] = CELL_EMPTY
        self.agent_positions[agent_id] = (new_x, new_y)
        self.dynamic_layer[new_x, new_y] = CELL_PERSON
        return True

    def remove_agent(self, agent_id):
        """Remove agent from grid."""
        if agent_id not in self.agent_positions:
            return False
        x, y = self.agent_positions[agent_id]
        self.dynamic_layer[x, y] = CELL_EMPTY
        del self.agent_positions[agent_id]
        return True

    def get_neighbors_8(self, x, y):
        """Get all 8-neighbor coordinates around (x, y)."""
        neighbors = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    neighbors.append((nx, ny))
        return neighbors

    def get_cell_type(self, x, y):
        """Get static cell type at position."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return None
        return self.static_layer[x, y]

    def set_cell_type(self, x, y, cell_type):
        """Set static cell type at position."""
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
        self.static_layer[x, y] = cell_type
        return True

    def get_all_exits(self):
        """Get all exit cell positions."""
        exits = []
        for x in range(self.width):
            for y in range(self.height):
                if self.static_layer[x, y] == CELL_EXIT:
                    exits.append((x, y))
        return exits

    def get_all_entrances(self):
        """Get all entrance cell positions."""
        entrances = []
        for x in range(self.width):
            for y in range(self.height):
                if self.static_layer[x, y] == CELL_ENTRANCE:
                    entrances.append((x, y))
        return entrances

    def get_grid_snapshot(self):
        """Get combined visualization layer (static + dynamic)."""
        # Start with static layer
        snapshot = self.static_layer.copy()

        # Overlay person positions
        for x, y in self.agent_positions.values():
            if snapshot[x, y] == CELL_EMPTY:
                snapshot[x, y] = CELL_PERSON

        return snapshot
