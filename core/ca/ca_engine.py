"""Main cellular automaton simulation engine."""
from .ca_grid import CAGrid
from .ca_agent import CAAgent
from .ca_environment import CAEnvironment
from .ca_behaviors import select_next_cell, resolve_conflicts, execute_moves, get_movement_statistics


class CASimulation:
    """Cellular automaton based evacuation simulation."""

    def __init__(self, width=100, height=100, max_timesteps=1000):
        """Initialize CA simulation.

        Args:
            width: Grid width (default 100)
            height: Grid height (default 100)
            max_timesteps: Maximum simulation steps (default 1000)
        """
        self.width = width
        self.height = height
        self.max_timesteps = max_timesteps
        self.timestep = 0

        # Initialize grid and environment
        self.grid = CAGrid(width, height)
        self.environment = CAEnvironment(self.grid)

        # Agent tracking
        self.agents = []
        self.evacuated_agents = []

        # Statistics
        self.history = {
            'timesteps': [],
            'active_agents': [],
            'evacuated_agents': [],
            'avg_panic': [],
            'max_panic': [],
            'avg_stamina': [],
        }

    def add_agent(self, agent_id, x, y, age=None, family_id=None):
        """Add agent to simulation at initial position."""
        if not self.grid.is_walkable(x, y):
            return False

        agent = CAAgent(agent_id, x, y, age, family_id)
        self.agents.append(agent)
        self.grid.place_agent(agent_id, x, y)
        return True

    def add_agents_random(self, count):
        """Add random agents at random walkable positions."""
        import random
        import numpy as np

        placed = 0
        attempts = 0
        max_attempts = count * 10

        while placed < count and attempts < max_attempts:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.grid.is_walkable(x, y) and not self.grid.is_occupied(x, y):
                age = random.randint(5, 80)
                family_id = random.randint(0, count // 5)
                self.add_agent(placed, x, y, age, family_id)
                placed += 1

            attempts += 1

        return placed

    def step(self):
        """Execute one simulation step.

        3-stage process:
        1. Intention registration: each agent selects next cell
        2. Conflict resolution: resolve multiple agents targeting same cell
        3. Execution: execute approved moves and update states
        """
        if self.timestep >= self.max_timesteps:
            return False

        # Load exits/entrances from grid
        self.environment.load_from_grid()

        # Stage 1: Intention registration
        intention_map = {}  # {agent_id: (x, y)}
        for agent in self.agents:
            if agent.evacuated:
                continue

            # Select next cell based on 8-neighborhood
            next_cell = select_next_cell(agent, self.environment, self.agents, self.grid)
            intention_map[agent.id] = next_cell

        # Stage 2: Conflict resolution
        approved_moves = resolve_conflicts(intention_map, self.agents, self.grid)

        # Stage 3: Execution
        newly_evacuated = execute_moves(self.agents, approved_moves, self.grid, self.environment)
        self.evacuated_agents.extend(newly_evacuated)

        # Update statistics
        self._update_statistics()

        self.timestep += 1
        return True

    def _update_statistics(self):
        """Update simulation statistics."""
        active = [a for a in self.agents if not a.evacuated]
        stats = get_movement_statistics(self.agents)

        self.history['timesteps'].append(self.timestep)
        self.history['active_agents'].append(len(active))
        self.history['evacuated_agents'].append(len(self.evacuated_agents))
        self.history['avg_panic'].append(stats['avg_panic'])
        self.history['max_panic'].append(stats['max_panic'])
        self.history['avg_stamina'].append(stats['avg_stamina'])

    def run(self, logger=None):
        """Run complete simulation until all evacuated or max steps reached.

        Args:
            logger: Optional CALogger to record each step

        Returns:
            Number of steps executed
        """
        while self.timestep < self.max_timesteps:
            # Check if all evacuated
            if len(self.evacuated_agents) == len(self.agents):
                print(f"All agents evacuated at timestep {self.timestep}")
                break

            # Execute step
            self.step()

            # Log if provided
            if logger:
                logger.log_step(
                    self.timestep,
                    self.agents,
                    self.grid,
                    self.get_statistics()
                )

            # Progress feedback
            if self.timestep % 100 == 0:
                print(f"Timestep {self.timestep}: "
                      f"Active={len([a for a in self.agents if not a.evacuated])}, "
                      f"Evacuated={len(self.evacuated_agents)}")

        return self.timestep

    def get_statistics(self):
        """Get current simulation statistics."""
        active = [a for a in self.agents if not a.evacuated]
        return {
            'timestep': self.timestep,
            'active_agents': len(active),
            'evacuated_agents': len(self.evacuated_agents),
            'avg_panic': sum(a.panic_level for a in active) / len(active) if active else 0.0,
            'max_panic': max((a.panic_level for a in active), default=0.0),
            'avg_stamina': sum(a.stamina for a in active) / len(active) if active else 1.0,
        }

    def get_grid_snapshot(self):
        """Get current grid state for visualization."""
        return self.grid.get_grid_snapshot()
