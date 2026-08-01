
def round_robin_agent(observation, configuration):
    return observation.step % configuration.banditCount

