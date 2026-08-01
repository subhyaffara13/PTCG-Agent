
def get_vision(robot_type, config):
    if robot_type == FACTORY:
        return config.visionFactory
    elif robot_type == SCOUT:
        return config.visionScout
    elif robot_type == WORKER:
        return config.visionWorker
    elif robot_type == MINER:
        return config.visionMiner
    return 0

