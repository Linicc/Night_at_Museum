"""Main entry point for CA-based evacuation simulation."""
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
from config import ca_settings
from core.ca.ca_engine import CASimulation
from core.ca.ca_grid import (
    CELL_EMPTY, CELL_PERSON, CELL_WALL, CELL_EXIT,
    CELL_ENTRANCE, CELL_EXHIBIT, CELL_EXHIBIT_SPECIAL, CELL_SECURITY
)
from io_manager.excel_parser import parse_excel_config, create_empty_config_template
from io_manager.excel_writer import create_output_workbook
from analysis.ca_logger import CALogger


def main():
    """Run CA simulation from Excel configuration."""
    print("=" * 60)
    print("Cellular Automaton Museum Evacuation Simulation")
    print("=" * 60)

    # Create output directory
    os.makedirs(ca_settings.OUTPUT_DIR, exist_ok=True)

    # Check if config file exists, if not create template
    if not os.path.exists(ca_settings.CONFIG_FILE):
        print(f"\nConfig file not found: {ca_settings.CONFIG_FILE}")
        print("Creating empty template...")
        create_empty_config_template(ca_settings.CONFIG_FILE)
        print(f"Template created at {ca_settings.CONFIG_FILE}")
        print("Please edit the template to configure the simulation and run again.")
        return

    # Parse configuration
    print(f"\nLoading configuration from {ca_settings.CONFIG_FILE}...")
    try:
        config = parse_excel_config(ca_settings.CONFIG_FILE)
    except Exception as e:
        print(f"Error loading config: {e}")
        return

    width = config['width']
    height = config['height']
    params = config['params']

    print(f"Grid size: {width} × {height}")
    print(f"Simulation steps: {params['simulation_steps']}")
    print(f"Initial population: {params['initial_population']}")

    # Initialize simulation
    print("\nInitializing simulation...")
    sim = CASimulation(width, height, max_timesteps=params['simulation_steps'])

    # Load grid from config
    for x in range(width):
        for y in range(height):
            if x < len(config['grid_data']) and y < len(config['grid_data'][x]):
                cell_type = config['grid_data'][x][y]
                if cell_type != CELL_EMPTY:
                    sim.grid.set_cell_type(x, y, cell_type)

    # Add agents from configuration
    if config['agents']:
        print(f"Loading {len(config['agents'])} agents from config...")
        for agent_data in config['agents']:
            sim.add_agent(
                agent_data['id'],
                agent_data['x'],
                agent_data['y'],
                agent_data.get('age'),
                agent_data.get('family_id')
            )
    else:
        # Random agent placement if no initial state specified
        print(f"Placing {params['initial_population']} agents randomly...")
        placed = sim.add_agents_random(params['initial_population'])
        print(f"Placed {placed} agents")

    # Initialize logger
    logger = CALogger()

    # Load environment (exits, entrances)
    sim.environment.load_from_grid()
    print(f"Found {len(sim.environment.exits)} exits and {len(sim.environment.entrances)} entrances")

    # Run simulation
    print("\nRunning simulation...")
    print("-" * 60)
    total_steps = sim.run(logger=logger)

    print("-" * 60)
    print(f"\nSimulation complete after {total_steps} timesteps")

    # Get summary statistics
    summary_stats = logger.get_summary_stats()
    print("\nSummary Statistics:")
    print(f"  Total agents: {summary_stats['total_agents']}")
    print(f"  Evacuated: {summary_stats['evacuated_agents']}")
    print(f"  Evacuation rate: {summary_stats['evacuation_rate']*100:.1f}%")
    if summary_stats['evacuation_time'] is not None:
        print(f"  First evacuation at step: {summary_stats['evacuation_time']}")
    print(f"  Average final panic: {summary_stats['avg_panic_final']:.3f}")
    print(f"  Max final panic: {summary_stats['max_panic_final']:.3f}")

    # Save results
    print("\nSaving results...")

    # Save agent trajectories to CSV
    csv_path = os.path.join(ca_settings.OUTPUT_DIR, "ca_simulation_log.csv")
    logger.save_to_csv(csv_path)
    print(f"  Agent trajectories saved to {csv_path}")

    # Save statistics to CSV
    stats_csv_path = os.path.join(ca_settings.OUTPUT_DIR, "ca_statistics.csv")
    logger.save_statistics_csv(stats_csv_path)
    print(f"  Statistics saved to {stats_csv_path}")

    # Save results to Excel
    excel_path = os.path.join(ca_settings.OUTPUT_DIR, "ca_simulation_results.xlsx")
    logger_data = logger.records
    create_output_workbook(sim, logger_data, excel_path)
    print(f"  Results saved to {excel_path}")

    # Generate heatmaps
    print("\nGenerating heatmaps...")
    _generate_heatmaps(logger, width, height)

    print("\n" + "=" * 60)
    print("Simulation completed successfully!")
    print(f"Results saved to {ca_settings.OUTPUT_DIR}/")
    print("=" * 60)


def _generate_heatmaps(logger, width, height):
    """Generate and save heatmap visualizations."""
    try:
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))

        # Crowding heatmap
        crowding = logger.get_crowding_heatmap(width, height)
        im1 = axes[0].imshow(crowding.T, cmap='hot', origin='lower')
        axes[0].set_title('Crowding Density Heatmap')
        axes[0].set_xlabel('X')
        axes[0].set_ylabel('Y')
        plt.colorbar(im1, ax=axes[0], label='Visits per timestep')

        # Panic heatmap
        panic = logger.get_panic_heatmap(width, height)
        im2 = axes[1].imshow(panic.T, cmap='RdYlGn_r', origin='lower', vmin=0, vmax=1)
        axes[1].set_title('Panic Level Heatmap')
        axes[1].set_xlabel('X')
        axes[1].set_ylabel('Y')
        plt.colorbar(im2, ax=axes[1], label='Average Panic Level')

        heatmap_path = os.path.join(ca_settings.OUTPUT_DIR, "ca_heatmap.png")
        plt.tight_layout()
        plt.savefig(heatmap_path, dpi=100)
        plt.close()
        print(f"  Heatmap saved to {heatmap_path}")
    except Exception as e:
        print(f"  Warning: Could not generate heatmap: {e}")


if __name__ == "__main__":
    main()
