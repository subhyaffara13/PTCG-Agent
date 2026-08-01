
def get_robot_max_energy(robot_type, config):
    if robot_type == FACTORY:
        return float("inf")
    elif robot_type == SCOUT:
        return config.scoutMaxEnergy
    elif robot_type == WORKER:
        return config.workerMaxEnergy
    elif robot_type == MINER:
        return config.minerMaxEnergy
    return 0

