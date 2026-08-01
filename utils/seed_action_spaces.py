
def seed_action_spaces(env):
    if hasattr(env, "agents"):
        for i, agent in enumerate(env.agents):
            env.action_space(agent).seed(42 + i)

