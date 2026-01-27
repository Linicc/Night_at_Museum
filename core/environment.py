import numpy as np

class Environment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 0: Empty, 1: Wall, 2: Exit, 3: Entrance, 4: Exhibit
        self.grid = np.zeros((width, height), dtype=int) 
        self.exits = []
        self.entrances = []
        self.obstacles = []
        self.exhibits = [] # List of (x, y, attractiveness)
        
    def add_wall(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = 1
            self.obstacles.append((x, y))
            
    def add_exit(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = 2
            self.exits.append((x, y))
            
    def add_entrance(self, x, y):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = 3
            self.entrances.append((x, y))
            
    def add_exhibit(self, x, y, is_special=False):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[x, y] = 4
            attr = 1.5 if is_special else 1.0
            self.exhibits.append({'pos': (x, y), 'attractiveness': attr, 'special': is_special})
            
    def is_walkable(self, x, y):
        # Assuming grid coordinates are integers
        ix, iy = int(x), int(y)
        if 0 <= ix < self.width and 0 <= iy < self.height:
            return self.grid[ix, iy] != 1
        return False
