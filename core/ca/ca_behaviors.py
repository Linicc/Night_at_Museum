"""Movement behaviors and conflict resolution for CA simulation."""
import random


def calculate_cell_attractiveness(x, y, agent, environment, agents):
    """Calculate attractiveness score for a cell.

    Combines:
    - Distance to exit (lower is better)
    - Crowding penalty (fewer agents is better)
    - Agent's panic level (high panic = more desperate to move anywhere)
    """
    # Basic distance to exit (normalized by grid size)
    exit_distance = environment.get_distance_to_exit(x, y)
    exit_attraction = -exit_distance  # Negative: closer exits are more attractive

    # Crowding penalty: count nearby agents
    crowd_count = environment.count_nearby_agents(x, y, radius=3)
    crowding_penalty = -crowd_count * 2.0

    # Panic factor: high panic agents are less discriminating
    panic_bonus = agent.panic_level * 1.0

    attractiveness = exit_attraction + crowding_penalty + panic_bonus
    return attractiveness


def select_next_cell(agent, environment, agents, grid):
    """Select next cell for agent to move to.

    Strategy:
    - Get all 8 neighbors
    - Calculate attractiveness of each
    - 80% chance: pick best cell (greedy)
    - 20% chance: pick random cell (exploration)
    - If high panic (>0.6): 40% random choice instead
    """
    current_x, current_y = agent.x, agent.y
    neighbors = grid.get_neighbors_8(current_x, current_y)

    # Filter to walkable neighbors
    walkable_neighbors = []
    for nx, ny in neighbors:
        if grid.is_walkable(nx, ny):
            walkable_neighbors.append((nx, ny))

    if not walkable_neighbors:
        # No escape, stay in place
        return (current_x, current_y)

    # Calculate attractiveness for each neighbor
    attractiveness_scores = []
    for nx, ny in walkable_neighbors:
        score = calculate_cell_attractiveness(nx, ny, agent, environment, agents)
        attractiveness_scores.append((score, (nx, ny)))

    # Sort by attractiveness (highest first)
    attractiveness_scores.sort(reverse=True, key=lambda x: x[0])

    # Decision: greedy vs random
    if agent.panic_level > 0.6:
        # High panic: 40% chance of random choice
        random_choice_prob = 0.4
    else:
        # Normal: 20% chance of random choice
        random_choice_prob = 0.2

    if random.random() < random_choice_prob:
        # Random choice from walkable neighbors
        return random.choice(walkable_neighbors)
    else:
        # Greedy: pick best cell
        return attractiveness_scores[0][1]


def resolve_conflicts(intention_map, agents, grid):
    """Resolve conflicts when multiple agents want same cell.

    Conflict resolution by priority:
    1. Children (age < 15): priority 1.5x
    2. Elderly (age > 65): priority 1.3x
    3. High panic: +0.5 to priority
    4. Random tiebreaker

    Only one agent per cell is allowed.
    """
    # Group intentions by target cell
    cell_to_agents = {}
    for agent in agents:
        target = intention_map.get(agent.id, (agent.x, agent.y))
        if target not in cell_to_agents:
            cell_to_agents[target] = []
        cell_to_agents[target].append(agent)

    # Resolve conflicts for cells with multiple agents
    approved_moves = {}  # {agent_id: (new_x, new_y) or None}

    for target_cell, candidates in cell_to_agents.items():
        if len(candidates) == 1:
            # No conflict
            approved_moves[candidates[0].id] = target_cell
        else:
            # Conflict: apply priority rules
            priority_scores = []
            for agent in candidates:
                priority = agent.get_priority()
                # Add random component for tiebreaker
                priority += random.random() * 0.1
                priority_scores.append((priority, agent))

            # Sort by priority (highest first)
            priority_scores.sort(reverse=True, key=lambda x: x[0])

            # Winner gets the cell
            winner = priority_scores[0][1]
            approved_moves[winner.id] = target_cell

            # Losers stay in place
            for _, agent in priority_scores[1:]:
                approved_moves[agent.id] = (agent.x, agent.y)

    return approved_moves


def execute_moves(agents, approved_moves, grid, environment):
    """Execute approved moves and update agent positions.

    Updates panic and stamina after movement.
    """
    evacuated_agents = []

    for agent in agents:
        if agent.evacuated:
            continue

        if agent.id not in approved_moves:
            continue

        new_x, new_y = approved_moves[agent.id]

        # Check if reached exit
        if grid.get_cell_type(new_x, new_y) == 3:  # CELL_EXIT
            agent.evacuated = True
            grid.remove_agent(agent.id)
            evacuated_agents.append(agent.id)
            continue

        # Move agent
        if new_x != agent.x or new_y != agent.y:
            agent.last_move_successful = grid.move_agent(agent.id, new_x, new_y)
            agent.move_to(new_x, new_y)
        else:
            agent.last_move_successful = False

        # Update panic based on nearby agents
        nearby_panic = environment.get_avg_panic_nearby(agent.x, agent.y, agents)
        agent.update_panic(nearby_panic)
        agent.decay_panic(rate=0.01)

    return evacuated_agents


def get_movement_statistics(agents):
    """Calculate movement statistics for logging."""
    if not agents:
        return {
            'avg_panic': 0.0,
            'max_panic': 0.0,
            'evacuated_count': 0,
            'total_count': 0,
            'avg_stamina': 1.0,
        }

    active_agents = [a for a in agents if not a.evacuated]
    total_agents = len([a for a in agents if not a.evacuated])

    avg_panic = sum(a.panic_level for a in active_agents) / len(active_agents) if active_agents else 0.0
    max_panic = max((a.panic_level for a in active_agents), default=0.0)
    avg_stamina = sum(a.stamina for a in active_agents) / len(active_agents) if active_agents else 1.0

    return {
        'avg_panic': avg_panic,
        'max_panic': max_panic,
        'evacuated_count': sum(1 for a in agents if a.evacuated),
        'total_count': total_agents,
        'avg_stamina': avg_stamina,
    }
