from typing import Any

def _seeded_observations(env_name: str, n: int = 5) -> list[dict[str, Any]]:
    """Build N observations from a few seeded steps of the env for parity checks."""
    obs_list: list[dict[str, Any]] = []
    for seed in range(n):
        env = make(env_name, configuration={"seed": seed}, debug=False)
        # Trigger interpreter to populate per-agent observation.
        env.reset()
        # First state with a real current player. For OpenSpiel-backed
        # envs the proxy obs lives on env.state[player].observation.
        for player_idx in range(len(env.state)):
            agent_state = env.state[player_idx]
            obs = agent_state.observation
            if not obs:
                continue
            d = dict(obs) if isinstance(obs, dict) else dict(vars(obs))
            d.setdefault("playerId", player_idx)
            obs_list.append(d)
            break
    return obs_list

