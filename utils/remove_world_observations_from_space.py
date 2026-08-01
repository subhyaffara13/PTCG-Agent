
def remove_world_observations_from_space(observation: spaces.Dict) -> spaces.Dict:
    """Removes the world observations key from a Gymnasium observation dict.

    This is used to limit the information an individual agent has access to (it cannot see the entire world).

    Args:
        observation: The Melting Pot observation

    Returns:
        observation: The Melting Pot observation, without world observations.
    """
    return spaces.Dict(
        {key: observation[key] for key in observation if _WORLD_PREFIX not in key}
    )

