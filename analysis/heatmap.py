import numpy as np
import matplotlib.pyplot as plt

def generate_density_heatmap(df, width, height, cell_size=1.0):
    # Bin x, y into grid
    x_bins = np.arange(0, width + cell_size, cell_size)
    y_bins = np.arange(0, height + cell_size, cell_size)
    
    # Simple histogram2d for all time steps combined
    # This represents accumulated occupancy
    H, xedges, yedges = np.histogram2d(df['x'], df['y'], bins=(x_bins, y_bins))
    
    return H.T # Transpose for correct orientation

def plot_heatmap(heatmap, output_path=None):
    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap, origin='lower', cmap='hot', interpolation='nearest')
    plt.colorbar(label='Density (Agent-Ticks)')
    plt.title("Crowd Density Heatmap")
    if output_path:
        plt.savefig(output_path)
    else:
        plt.close() # Close to free memory if not showing
