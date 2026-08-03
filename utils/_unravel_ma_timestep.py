from typing import Any

def _unravel_ma_timestep(timestep: dm_env.TimeStep, agents: list[AgentID]) -> tuple[
    dict[AgentID, Any],
    dict[AgentID, float],
    dict[AgentID, bool],
    dict[AgentID, bool],
    dict[AgentID, Any],
]:
    """Opens up the timestep to return obs, reward, terminated, truncated, info."""
    # set terminated and truncated
    term, trunc = False, False
    if timestep.last():
        if timestep.discount == 0:
            trunc = True
        else:
            term = True

    # expand the observations
    list_observations = [dm_obs2gym_obs(obs) for obs in timestep.observation]
    observations: dict[AgentID, Any] = dict(zip(agents, list_observations))

    # sometimes deepmind decides not to reward people
    rewards: dict[AgentID, float] = {agent: 0.0 for agent in agents}

    if timestep.reward:
        rewards = dict(zip(agents, timestep.reward))

    # expand everything else
    terminations: dict[AgentID, bool] = {agent: term for agent in agents}
    truncations: dict[AgentID, bool] = {agent: trunc for agent in agents}

    # duplicate infos across agents
    infos = {
        agent: {
            "timestep.discount": timestep.discount,
            "timestep.step_type": timestep.step_type,
        }
        for agent in agents
    }

    return (
        observations,
        rewards,
        terminations,
        truncations,
        infos,
    )

