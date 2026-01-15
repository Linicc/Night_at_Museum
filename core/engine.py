from .agent import Agent
from .environment import Environment
from .behaviors import apply_social_force
import numpy as np

class Simulation:
    def __init__(self, width, height, num_agents, dt=0.1):
        self.environment = Environment(width, height)
        self.agents = []
        self.time = 0
        self.dt = dt
        self._init_agents(num_agents)
        
    def _init_agents(self, num):
        for i in range(num):
            # Random position (simple rejection sampling for validity)
            while True:
                pos = [np.random.uniform(1, self.environment.width-1), 
                       np.random.uniform(1, self.environment.height-1)]
                if self.environment.is_walkable(pos[0], pos[1]):
                    self.agents.append(Agent(i, pos))
                    break
            
    def step(self):
        # 1. Update Behaviors
        # In a real large simulation, use a spatial index (KDTree or Grid) for neighbors
        # Here we just iterate all for simplicity (O(N^2))
        for agent in self.agents:
            neighbors = self.agents 
            acc = apply_social_force(agent, neighbors, self.environment)
            agent.vel += acc * self.dt
            agent.set_velocity(agent.vel) # Clamp speed
            
        # 2. Move
        for agent in self.agents:
            new_pos = agent.pos + agent.vel * self.dt
            # Basic bound check
            if (0 <= new_pos[0] < self.environment.width and 
                0 <= new_pos[1] < self.environment.height and
                self.environment.is_walkable(new_pos[0], new_pos[1])):
                agent.pos = new_pos
            else:
                # Simple bounce or stop
                agent.vel = np.array([0.0, 0.0])
                
        self.time += self.dt
        return self.agents
