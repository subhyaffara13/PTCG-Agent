from typing import Any

def _check_observation_saveable(
    env: AECEnv[AgentID, Any, Any] | ParallelEnv[AgentID, Any, Any], agent: AgentID
) -> None:
    obs_space = env.observation_space(agent)
    assert isinstance(
        obs_space, gymnasium.spaces.Box
    ), "Observations must be Box to save observations as image"
    assert np.all(np.equal(obs_space.low, 0)) and np.all(
        np.equal(obs_space.high, 255)
    ), "Observations must be 0 to 255 to save as image"
    assert (
        len(obs_space.shape) == 3 or len(obs_space.shape) == 2
    ), "Observations must be 2D or 3D to save as image"
    if len(obs_space.shape) == 3:
        assert (
            obs_space.shape[2] == 1 or obs_space.shape[2] == 3
        ), "3D observations can only have 1 or 3 channels to save as an image"

