import pandas as pd
import numpy as np

class SimulationLogger:
    def __init__(self):
        self.data = []
        
    def log_step(self, time, agents):
        for agent in agents:
            self.data.append({
                'time': time,
                'id': agent.id,
                'x': agent.pos[0],
                'y': agent.pos[1],
                'vx': agent.vel[0],
                'vy': agent.vel[1],
                'panic': agent.panic_level
            })
            
    def save_to_csv(self, filename):
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False)
        return df
