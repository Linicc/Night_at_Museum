import numpy as np
import random

class Agent:
    def __init__(self, id, pos, family_id=None, age=None):
        self.id = id
        self.pos = np.array(pos, dtype=float)
        self.vel = np.array([0.0, 0.0])
        self.family_id = family_id
        
        # Attributes based on Age (simplified logic)
        self.age = age if age else random.randint(5, 80)
        self._init_attributes_by_age()
        
        # State
        self.panic_level = 0.0
        self.target = None
        self.stamina = 1.0 # 1.0 is full
        
    def _init_attributes_by_age(self):
        # Simplified age effect
        if 20 <= self.age <= 40:
            self.max_speed = 1.5 + random.uniform(-0.2, 0.2)
            self.reaction_time = 0.2
            self.resilience = 0.8
        elif self.age < 10 or self.age > 70:
            self.max_speed = 0.8 + random.uniform(-0.1, 0.1)
            self.reaction_time = 0.8
            self.resilience = 0.3
        else:
            self.max_speed = 1.2 + random.uniform(-0.2, 0.2)
            self.reaction_time = 0.4
            self.resilience = 0.5
            
    def update_panic(self, danger_proximity, surrounding_panic):
        # Panic increases with danger and surrounding panic, decreases with resilience
        infection = surrounding_panic * (1.0 - self.resilience)
        self.panic_level = min(1.0, self.panic_level + infection + danger_proximity)
        
    def set_velocity(self, desired_vel):
        # Limit speed based on max_speed and panic factor (panic can increase speed slightly but reduce control - here just speed)
        current_max = self.max_speed * (1.0 + 0.2 * self.panic_level)
        speed = np.linalg.norm(desired_vel)
        if speed > current_max:
            self.vel = (desired_vel / speed) * current_max
        else:
            self.vel = desired_vel
            
    def move(self, dt):
        self.pos += self.vel * dt
