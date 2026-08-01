
def timestep_to_observations(timestep: dm_env.TimeStep) -> ObsDict:
    """Extracts Gymnasium-compatible observations from a Melting Pot timestep.

    Args:
        timestep: The dm_env timestep

    Returns:
        observation, reward, terminated, truncated, info.
    """
    gym_observations = {}
    for index, observation in enumerate(timestep.observation):
        gym_observations[PLAYER_STR_FORMAT.format(index=index)] = {
            key: value for key, value in observation.items() if _WORLD_PREFIX not in key
        }
    return gym_observations

