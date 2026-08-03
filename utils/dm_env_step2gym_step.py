from typing import Any

def dm_env_step2gym_step(timestep) -> tuple[Any, float, bool, bool, dict[str, Any]]:
    """Converts a dm_env timestep to the required return info from Gymnasium step() function.

    Args:
        timestep: The dm_env timestep

    Returns:
        observation, reward, terminated, truncated, info.
    """
    obs = dm_obs2gym_obs(timestep.observation)
    reward = timestep.reward or 0

    # set terminated and truncated
    terminated, truncated = False, False
    if timestep.last():
        # https://github.com/deepmind/dm_env/blob/master/docs/index.md#example-sequences
        if timestep.discount > 0:
            truncated = True
        else:
            terminated = True

    info = {
        "timestep.discount": timestep.discount,
        "timestep.step_type": timestep.step_type,
    }

    return (
        obs,
        reward,
        terminated,
        truncated,
        info,
    )

