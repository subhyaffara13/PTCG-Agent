
def check_environment_deterministic_parallel(env1, env2, num_cycles):
    """Check that two parallel environments execute the same way."""
    env1.reset(seed=42)
    env2.reset(seed=42)

    # seed action spaces to ensure sampled actions are the same
    seed_action_spaces(env1)
    seed_action_spaces(env2)

    # seed observation spaces to ensure first observation is the same
    seed_observation_spaces(env1)
    seed_observation_spaces(env2)

    iter = 0
    max_env_iters = num_cycles * len(env1.agents)

    env1.reset(seed=42)
    env2.reset(seed=42)

    seed_action_spaces(env1)
    seed_action_spaces(env2)

    while env1.agents:
        actions1 = {agent: env1.action_space(agent).sample() for agent in env1.agents}
        actions2 = {agent: env2.action_space(agent).sample() for agent in env2.agents}

        assert data_equivalence(actions1, actions2), "Incorrect action seeding"

        obs1, rewards1, terminations1, truncations1, infos1 = env1.step(actions1)
        obs2, rewards2, terminations2, truncations2, infos2 = env2.step(actions2)

        iter += 1

        assert data_equivalence(obs1, obs2), "Incorrect observations"
        assert data_equivalence(rewards1, rewards2), "Incorrect values for rewards"
        assert data_equivalence(terminations1, terminations2), "Incorrect terminations."
        assert data_equivalence(truncations1, truncations2), "Incorrect truncations"
        assert data_equivalence(infos1, infos2), "Incorrect infos"

        if iter >= max_env_iters or any(terminations1) or any(truncations1):
            break

    env1.close()
    env2.close()

