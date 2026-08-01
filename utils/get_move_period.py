
def get_move_period(robot_type, config):
    if robot_type == FACTORY:
        return config.factoryMovePeriod
    elif robot_type == SCOUT:
        return 1
    elif robot_type == WORKER:
        return config.workerMovePeriod
    elif robot_type == MINER:
        return config.minerMovePeriod
    return 1

