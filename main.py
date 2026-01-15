import os
from config import settings
from core.engine import Simulation
from analysis.logger import SimulationLogger
from analysis.heatmap import generate_density_heatmap, plot_heatmap

def main():
    print("Initializing Simulation...")
    # Setup
    sim = Simulation(settings.GRID_WIDTH, settings.GRID_HEIGHT, num_agents=50, dt=settings.TIME_STEP)
    
    # Add exits and obstacles (Sample layout)
    # Exit at the right middle
    sim.environment.add_exit(settings.GRID_WIDTH-1, settings.GRID_HEIGHT // 2)
    
    # Add a central obstacle
    for i in range(40, 60):
        for j in range(40, 60):
            sim.environment.add_wall(i, j)
            
    logger = SimulationLogger()
    
    print("Running Simulation...")
    for step in range(settings.MAX_STEPS):
        agents = sim.step()
        logger.log_step(sim.time, agents)
        
        if step % 100 == 0:
            print(f"Step {step}/{settings.MAX_STEPS}")
            
    print("Simulation Complete.")
    
    # Save Data
    output_dir = "output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    df = logger.save_to_csv(os.path.join(output_dir, "simulation_log.csv"))
    print(f"Data saved to {output_dir}/simulation_log.csv")
    
    # Generate Heatmap
    heatmap = generate_density_heatmap(df, settings.GRID_WIDTH, settings.GRID_HEIGHT)
    plot_heatmap(heatmap, os.path.join(output_dir, "heatmap.png"))
    print(f"Heatmap saved to {output_dir}/heatmap.png")

if __name__ == "__main__":
    main()
