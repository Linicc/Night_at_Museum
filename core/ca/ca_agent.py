"""Discrete grid agent for cellular automaton simulation."""
import random


class CAAgent:
    """Agent on discrete cellular grid."""

    def __init__(self, agent_id, x, y, age=None, family_id=None):
        """Initialize CA agent at grid position (x, y)."""
        self.id = agent_id
        self.x = x
        self.y = y
        self.age = age if age else random.randint(5, 80)
        self.family_id = family_id

        # Age-based attributes
        self._init_attributes_by_age()

        # State
        self.panic_level = 0.0  # 0.0 to 1.0
        self.evacuated = False  # Has reached exit
        self.stamina = 1.0  # 0.0 to 1.0
        self.last_move_successful = True

    def _init_attributes_by_age(self):
        """Initialize attributes based on age."""
        # Children (< 15): slower, more panic-prone
        if self.age < 15:
            self.base_speed = 0.7
            self.resilience = 0.3
            self.priority_multiplier = 1.5  # Higher priority in conflicts
        # Elderly (> 65): slower, less resilient
        elif self.age > 65:
            self.base_speed = 0.6
            self.resilience = 0.4
            self.priority_multiplier = 1.3
        # Young adults (20-40): faster, more resilient
        elif 20 <= self.age <= 40:
            self.base_speed = 1.0
            self.resilience = 0.8
            self.priority_multiplier = 1.0
        # Others
        else:
            self.base_speed = 0.9
            self.resilience = 0.6
            self.priority_multiplier = 1.0

    def update_panic(self, neighbors_panic, danger_proximity=0.0):
        """Update panic level based on surroundings and danger."""
        # Panic spreads from neighbors
        infection = neighbors_panic * (1.0 - self.resilience)
        # Direct danger increases panic
        danger_increase = danger_proximity * (1.0 - self.resilience)
        # Update
        self.panic_level = min(1.0, self.panic_level + infection + danger_increase)

    def decay_panic(self, rate=0.01):
        """Decrease panic over time (natural calm down)."""
        self.panic_level = max(0.0, self.panic_level - rate)

    def get_priority(self):
        """Get conflict resolution priority score."""
        # Base priority from age multiplier
        priority = self.priority_multiplier
        # High panic increases priority slightly
        priority += self.panic_level * 0.5
        return priority

    def get_effective_speed(self):
        """Get movement speed influenced by panic and stamina."""
        # Panic slightly increases speed (rushing) but reduces control
        speed_boost = self.panic_level * 0.2
        # Stamina reduces speed when low
        stamina_factor = 0.5 + 0.5 * self.stamina
        effective = self.base_speed * (1.0 + speed_boost) * stamina_factor
        return effective

    def can_move(self):
        """Check if agent can move (has stamina)."""
        return self.stamina > 0.0

    def move_to(self, x, y):
        """Update position (used after conflict resolution confirms move)."""
        self.x = x
        self.y = y
        self.stamina = max(0.0, self.stamina - 0.01)  # Small stamina cost

    def __repr__(self):
        return f"CAAgent(id={self.id}, pos=({self.x},{self.y}), panic={self.panic_level:.2f}, age={self.age})"
