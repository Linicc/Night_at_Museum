"""Logging system for CA simulation."""
import os
import pandas as pd
import numpy as np


class CALogger:
    """Log agent states and statistics during CA simulation."""

    def __init__(self):
        """Initialize logger."""
        self.records = []  # List of agent records
        self.timesteps = []  # List of timestep statistics

    def log_step(self, timestep, agents, grid, statistics):
        """Log all agents at a timestep.

        Args:
            timestep: Current simulation step
            agents: List of CAAgent instances
            grid: CAGrid instance
            statistics: Dict of current statistics
        """
        # Record each agent's state
        for agent in agents:
            record = {
                'timestep': timestep,
                'agent_id': agent.id,
                'x': agent.x,
                'y': agent.y,
                'panic_level': agent.panic_level,
                'evacuated': agent.evacuated,
                'age': agent.age,
                'stamina': agent.stamina,
                'family_id': agent.family_id,
            }
            self.records.append(record)

        # Record timestep statistics
        self.timesteps.append(statistics)

    def save_to_csv(self, output_path):
        """Save agent trajectories to CSV.

        Args:
            output_path: Path to save CSV file

        Returns:
            DataFrame of records
        """
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        df = pd.DataFrame(self.records)

        # Ensure timestep is first column and sorted
        if not df.empty:
            df = df.sort_values('timestep')

        df.to_csv(output_path, index=False)
        return df

    def save_statistics_csv(self, output_path):
        """Save timestep statistics to CSV.

        Args:
            output_path: Path to save CSV file

        Returns:
            DataFrame of statistics
        """
        os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)

        df = pd.DataFrame(self.timesteps)
        df.to_csv(output_path, index=False)
        return df

    def get_summary_stats(self):
        """Get overall simulation summary statistics."""
        if not self.records:
            return {}

        df = pd.DataFrame(self.records)

        evacuation_time = None
        if any(df['evacuated']):
            first_evacuation = df[df['evacuated']]['timestep'].min()
            evacuation_time = first_evacuation

        total_evacuated = len(df[df['evacuated']]['agent_id'].unique())
        total_agents = df['agent_id'].nunique()

        avg_panic_final = df[df['timestep'] == df['timestep'].max()]['panic_level'].mean()
        max_panic_final = df[df['timestep'] == df['timestep'].max()]['panic_level'].max()

        return {
            'total_agents': total_agents,
            'evacuated_agents': total_evacuated,
            'evacuation_rate': total_evacuated / max(1, total_agents),
            'evacuation_time': evacuation_time,
            'avg_panic_final': avg_panic_final,
            'max_panic_final': max_panic_final,
            'total_timesteps': df['timestep'].max(),
        }

    def get_agent_trajectory(self, agent_id):
        """Get complete trajectory for specific agent."""
        df = pd.DataFrame(self.records)
        return df[df['agent_id'] == agent_id].sort_values('timestep')

    def get_crowding_heatmap(self, width, height):
        """Generate crowding heatmap from agent positions.

        Args:
            width: Grid width
            height: Grid height

        Returns:
            2D numpy array of crowding density
        """
        if not self.records:
            return np.zeros((width, height))

        df = pd.DataFrame(self.records)

        # Count agents at each position across all timesteps
        heatmap = np.zeros((width, height))
        for _, row in df.iterrows():
            x, y = int(row['x']), int(row['y'])
            if 0 <= x < width and 0 <= y < height:
                heatmap[x, y] += 1

        # Normalize by number of timesteps
        max_count = df['timestep'].max() + 1
        if max_count > 0:
            heatmap = heatmap / max_count

        return heatmap

    def get_panic_heatmap(self, width, height):
        """Generate panic level heatmap.

        Args:
            width: Grid width
            height: Grid height

        Returns:
            2D numpy array of average panic levels
        """
        if not self.records:
            return np.zeros((width, height))

        df = pd.DataFrame(self.records)

        # Average panic level at each position
        heatmap = np.zeros((width, height))
        counts = np.zeros((width, height))

        for _, row in df.iterrows():
            x, y = int(row['x']), int(row['y'])
            if 0 <= x < width and 0 <= y < height:
                heatmap[x, y] += row['panic_level']
                counts[x, y] += 1

        # Average
        with np.errstate(divide='ignore', invalid='ignore'):
            heatmap = np.where(counts > 0, heatmap / counts, 0)

        return heatmap
