import numpy as np

def get_direction_to_nearest_exit(agent, environment):
    # Find nearest exit
    if not environment.exits:
        return np.array([0.0, 0.0])
    
    best_dist = float('inf')
    best_dir = np.array([0.0, 0.0])
    
    for exit_pos in environment.exits:
        # Vector from agent to exit
        vec = np.array(exit_pos) - agent.pos
        dist = np.linalg.norm(vec)
        if dist < best_dist:
            best_dist = dist
            best_dir = vec
            
    if best_dist > 0:
        return best_dir / best_dist
    return np.array([0.0, 0.0])

def apply_social_force(agent, neighbors, environment):
    # 1. Desire to exit
    desired_dir = get_direction_to_nearest_exit(agent, environment)
    desired_vel = desired_dir * agent.max_speed
    
    # 2. Repulsion from neighbors (Collision avoidance)
    repulsion = np.array([0.0, 0.0])
    for other in neighbors:
        if other.id == agent.id:
            continue
        dist_vec = agent.pos - other.pos
        dist = np.linalg.norm(dist_vec)
        if dist < 1.0 and dist > 0: # Personal space
            # Exponential repulsion
            repulsion += (dist_vec / dist) * 2.0 * np.exp(-dist / 0.3)
            
    # 3. Family cohesion (Attraction)
    attraction = np.array([0.0, 0.0])
    if agent.family_id is not None:
        for other in neighbors:
            if other.family_id == agent.family_id and other.id != agent.id:
                dist_vec = other.pos - agent.pos
                dist = np.linalg.norm(dist_vec)
                if dist > 2.0: # If too far, attract
                     attraction += (dist_vec / dist) * 1.5
    
    # Combine
    # F = ma -> a = F/m. Assuming m=1.
    # Force = (Desired - Current) / RelaxationTime + Repulsion + Attraction
    force_drive = (desired_vel - agent.vel) / agent.reaction_time
    total_acc = force_drive + repulsion + attraction
    
    return total_acc
