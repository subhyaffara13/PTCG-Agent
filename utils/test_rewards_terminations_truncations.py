
def test_rewards_terminations_truncations(env, agent_0):
    for agent in env.agents:
        assert isinstance(
            env.terminations[agent], bool
        ), "Agent's values in terminations must be True or False"
        assert isinstance(
            env.truncations[agent], bool
        ), "Agent's values in truncations must be True or False"
        float(
            env.rewards[agent]
        )  # "Rewards for each agent must be convertible to float
        test_reward(env.rewards[agent])

