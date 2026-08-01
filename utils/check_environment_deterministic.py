
def check_environment_deterministic(env1, env2, num_cycles):
    """Check that two AEC environments execute the same way."""

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

    for agent1, agent2 in zip(env1.agent_iter(), env2.agent_iter()):
        assert data_equivalence(agent1, agent2), f"Incorrect agent: {agent1} {agent2}"

        obs1, reward1, termination1, truncation1, info1 = env1.last()
        obs2, reward2, termination2, truncation2, info2 = env2.last()

        assert data_equivalence(obs1, obs2), "Incorrect observation"
        assert data_equivalence(reward1, reward2), "Incorrect reward."
        assert data_equivalence(termination1, termination2), "Incorrect termination."
        assert data_equivalence(truncation1, truncation2), "Incorrect truncation."
        assert data_equivalence(info1, info2), "Incorrect info."

        if termination1 or truncation1:
            break

        mask1 = obs1.get("action_mask") if isinstance(obs1, dict) else None
        mask2 = obs2.get("action_mask") if isinstance(obs2, dict) else None
        assert data_equivalence(mask1, mask2), f"Incorrect action mask: {mask1} {mask2}"

        action1 = env1.action_space(agent1).sample(mask1)
        action2 = env2.action_space(agent2).sample(mask2)

        assert data_equivalence(
            action1, action2
        ), f"Incorrect actions: {action1} {action2}"

        env1.step(action1)
        env2.step(action2)

        iter += 1

        if iter >= max_env_iters:
            break

    env1.close()
    env2.close()

