"""Demo script for CA simulation - tests core functionality without Excel."""
import os
import numpy as np
from core.ca.ca_engine import CASimulation
from core.ca.ca_grid import CELL_WALL, CELL_EXIT, CELL_ENTRANCE
from analysis.ca_logger import CALogger


def create_simple_layout(sim):
    """Create a simple museum layout for testing."""
    # Create walls around perimeter
    for x in range(sim.width):
        sim.grid.set_cell_type(x, 0, CELL_WALL)
        sim.grid.set_cell_type(x, sim.height - 1, CELL_WALL)

    for y in range(sim.height):
        sim.grid.set_cell_type(0, y, CELL_WALL)
        sim.grid.set_cell_type(sim.width - 1, y, CELL_WALL)

    # Create a central obstacle (exhibition area)
    for x in range(35, 65):
        for y in range(35, 65):
            sim.grid.set_cell_type(x, y, CELL_WALL)

    # Add entrances
    sim.environment.add_entrance(sim.width // 2, 1)

    # Add exits at corners
    sim.environment.add_exit(5, sim.height - 2)
    sim.environment.add_exit(sim.width - 6, sim.height - 2)
    sim.environment.add_exit(5, 5)
    sim.environment.add_exit(sim.width - 6, 5)

    print(f"Layout created with {len(sim.environment.exits)} exits and {len(sim.environment.entrances)} entrances")


def run_demo():
    """Run a simple demonstration of the CA system."""
    print("=" * 60)
    print("CA Evacuation Simulation - Demo")
    print("=" * 60)

    # Create simulation
    print("\n1. Creating simulation...")
    sim = CASimulation(width=100, height=100, max_timesteps=500)

    # Setup layout
    print("2. Setting up layout...")
    create_simple_layout(sim)

    # Add agents
    print("3. Adding agents...")
    num_agents = 75
    placed = sim.add_agents_random(num_agents)
    print(f"   Placed {placed} agents (target: {num_agents})")

    # Initialize logger
    print("4. Initializing logger...")
    logger = CALogger()

    # Run simulation
    print("5. Running simulation (this may take a moment)...")
    print("-" * 60)

    steps = 0
    last_active = num_agents

    while steps < 500:
        # Execute step
        sim.step()

        # Log state every step
        logger.log_step(sim.timestep, sim.agents, sim.grid, sim.get_statistics())

        # Print progress every 50 steps
        if sim.timestep % 50 == 0:
            active = len([a for a in sim.agents if not a.evacuated])
            evacuated = len(sim.evacuated_agents)
            print(f"Step {sim.timestep:4d}: Active={active:3d}, Evacuated={evacuated:3d}")

            # Stop early if all evacuated
            if active == 0:
                print(f"\nAll agents evacuated at step {sim.timestep}!")
                break

        steps += 1

    print("-" * 60)

    # Print results
    print("\n6. Results:")
    stats = logger.get_summary_stats()
    print(f"   Total timesteps: {stats['total_timesteps']}")
    print(f"   Total agents: {stats['total_agents']}")
    print(f"   Evacuated: {stats['evacuated_agents']}")
    print(f"   Evacuation rate: {stats['evacuation_rate']*100:.1f}%")
    if stats['evacuation_time']:
        print(f"   First evacuation at: step {stats['evacuation_time']}")
    print(f"   Avg panic (final): {stats['avg_panic_final']:.3f}")
    print(f"   Max panic (final): {stats['max_panic_final']:.3f}")

    # Save outputs
    print("\n7. Saving results...")
    os.makedirs("output", exist_ok=True)

    csv_path = "output/demo_ca_log.csv"
    logger.save_to_csv(csv_path)
    print(f"   CSV log saved: {csv_path}")

    stats_csv = "output/demo_ca_stats.csv"
    logger.save_statistics_csv(stats_csv)
    print(f"   Statistics saved: {stats_csv}")

    print("\n" + "=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)

    return sim, logger


if __name__ == "__main__":
    try:
        sim, logger = run_demo()
        print("\nYou can now:")
        print("1. Edit config/museum_ca_config.xlsx to create your own scenario")
        print("2. Run: python main_ca.py")
        print("3. Or run this demo again: python test_ca_demo.py")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
