
def seed_observation_spaces(env):
    if hasattr(env, "agents"):
        for i, agent in enumerate(env.agents):
            env.observation_space(agent).seed(42 + i)

