
def test_action_flexibility(env):
    """Tests that a given action is valid given a seeded environment reset"""
    env.reset(seed=0)
    agent = env.agent_selection
    action_space = env.action_space(agent)
    if isinstance(action_space, gymnasium.spaces.Discrete):
        obs, reward, terminated, truncated, info = env.last()
        if terminated or truncated:
            action = None
        elif isinstance(obs, dict) and "action_mask" in obs:
            action = env.action_space(agent).sample(obs["action_mask"])
        elif "action_mask" in info:
            action = env.action_space(agent).sample(info["action_mask"])
        else:
            action = 0
        env.step(action)
        env.reset(seed=0)
        env.step(np.int32(action))
    elif isinstance(action_space, gymnasium.spaces.Box):
        env.step(np.zeros_like(action_space.low))
        env.reset(seed=0)
        env.step(np.zeros_like(action_space.low))

