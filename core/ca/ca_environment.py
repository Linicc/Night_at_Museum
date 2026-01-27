"""Static environment management for CA simulation."""
from .ca_grid import CELL_EXIT, CELL_ENTRANCE


class CAEnvironment:
    """Manages static environment features (exits, entrances, walls, exhibits)."""

    def __init__(self, grid):
        """Initialize environment with reference to grid."""
        self.grid = grid
        self.exits = []
        self.entrances = []

    def load_from_grid(self):
        """Load exits and entrances from grid's static layer."""
        self.exits = self.grid.get_all_exits()
        self.entrances = self.grid.get_all_entrances()

    def add_exit(self, x, y):
        """Add exit point."""
        if self.grid.set_cell_type(x, y, CELL_EXIT):
            if (x, y) not in self.exits:
                self.exits.append((x, y))
            return True
        return False

    def add_entrance(self, x, y):
        """Add entrance point."""
        if self.grid.set_cell_type(x, y, CELL_ENTRANCE):
            if (x, y) not in self.entrances:
                self.entrances.append((x, y))
            return True
        return False

    def get_nearest_exit(self, x, y):
        """Find nearest exit using Manhattan distance."""
        if not self.exits:
            return None

        min_dist = float('inf')
        nearest = None
        for exit_x, exit_y in self.exits:
            # Use Manhattan distance for grid
            dist = abs(x - exit_x) + abs(y - exit_y)
            if dist < min_dist:
                min_dist = dist
                nearest = (exit_x, exit_y)

        return nearest

    def get_distance_to_exit(self, x, y):
        """Get Manhattan distance to nearest exit."""
        exit_pos = self.get_nearest_exit(x, y)
        if exit_pos is None:
            return float('inf')
        return abs(x - exit_pos[0]) + abs(y - exit_pos[1])

    def get_nearest_entrance(self, x, y):
        """Find nearest entrance using Manhattan distance."""
        if not self.entrances:
            return None

        min_dist = float('inf')
        nearest = None
        for entrance_x, entrance_y in self.entrances:
            dist = abs(x - entrance_x) + abs(y - entrance_y)
            if dist < min_dist:
                min_dist = dist
                nearest = (entrance_x, entrance_y)

        return nearest

    def count_nearby_agents(self, x, y, radius=5):
        """Count agents within radius."""
        count = 0
        for agent_x, agent_y in self.grid.agent_positions.values():
            dist = abs(x - agent_x) + abs(y - agent_y)
            if dist <= radius:
                count += 1
        return count

    def get_avg_panic_nearby(self, x, y, agents, radius=3):
        """Get average panic level of nearby agents."""
        if not agents:
            return 0.0

        nearby_panic = []
        for agent in agents:
            dist = abs(x - agent.x) + abs(y - agent.y)
            if dist <= radius:
                nearby_panic.append(agent.panic_level)

        if nearby_panic:
            return sum(nearby_panic) / len(nearby_panic)
        return 0.0
