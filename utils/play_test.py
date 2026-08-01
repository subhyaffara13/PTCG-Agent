
def play_test(env, observation_0, num_cycles):
    """
    plays through environment and does dynamic checks to make
    sure the state returned by the environment is
    consistent. In particular it checks:

    * Whether the reward returned by last is the accumulated reward
    * Whether the agents list shrinks when agents are terminated or truncated
    * Whether the keys of the rewards, terminations, truncations, infos are equal to the agents list
    * tests that the observation is in bounds.
    """
    env.reset()

    live_agents = set(env.agents[:])
    has_finished = set()
    generated_agents = set()
    accumulated_rewards = defaultdict(int)
    for agent in env.agent_iter(env.num_agents * num_cycles):
        generated_agents.add(agent)
        assert (
            agent not in has_finished
        ), "agents cannot resurect! Generate a new agent with a new name."
        assert isinstance(
            env.infos[agent], dict
        ), "an environment agent's info must be a dictionary"
        prev_observe, reward, terminated, truncated, info = env.last()
        if terminated or truncated:
            action = None
        elif isinstance(prev_observe, dict) and "action_mask" in prev_observe:
            action = env.action_space(agent).sample(prev_observe["action_mask"])
        elif "action_mask" in info:
            action = env.action_space(agent).sample(info["action_mask"])
        else:
            action = env.action_space(agent).sample()

        if agent not in live_agents:
            live_agents.add(agent)

        assert live_agents.issubset(
            set(env.agents)
        ), "environment must delete agents as the game continues"

        if terminated or truncated:
            live_agents.remove(agent)
            has_finished.add(agent)

        assert (
            accumulated_rewards[agent] == reward
        ), "reward returned by last is not the accumulated rewards in its rewards dict"
        accumulated_rewards[agent] = 0

        env.step(action)

        for a, rew in env.rewards.items():
            accumulated_rewards[a] += rew

        assert env.num_agents == len(
            env.agents
        ), "env.num_agents is not equal to len(env.agents)"
        assert set(env.rewards.keys()) == (
            set(env.agents)
        ), "agents should not be given a reward if they were terminated or truncated last turn"
        assert set(env.terminations.keys()) == (
            set(env.agents)
        ), "agents should not be given a termination if they were terminated or truncated last turn"
        assert set(env.truncations.keys()) == (
            set(env.agents)
        ), "agents should not be given a truncation if they were terminated or truncated last turn"
        assert set(env.infos.keys()) == (
            set(env.agents)
        ), "agents should not be given an info if they were terminated or truncated last turn"
        if hasattr(env, "possible_agents"):
            assert set(env.agents).issubset(
                set(env.possible_agents)
            ), "possible agents should always include all agents, if it exists"

        if not env.agents:
            break

        assert env.observation_space(agent).contains(
            prev_observe
        ), "Out of bounds observation: " + str(prev_observe)

        if isinstance(env.observation_space(agent), gymnasium.spaces.Box):
            assert env.observation_space(agent).dtype == prev_observe.dtype
        elif isinstance(env.observation_space(agent), gymnasium.spaces.Dict):
            assert (
                env.observation_space(agent)["observation"].dtype
                == prev_observe["observation"].dtype
            )
        test_observation(prev_observe, observation_0, str(env.unwrapped))
        if not isinstance(env.infos[env.agent_selection], dict):
            warnings.warn(
                "The info of each agent should be a dict, use {} if you aren't using info"
            )

    if not env.agents:
        assert (
            has_finished == generated_agents
        ), "not all agents finished, some were skipped over"

    env.reset()
    for agent in env.agent_iter(env.num_agents * 2):
        obs, reward, terminated, truncated, info = env.last()
        if terminated or truncated:
            action = None
        elif isinstance(obs, dict) and "action_mask" in obs:
            action = env.action_space(agent).sample(obs["action_mask"])
        elif "action_mask" in info:
            action = env.action_space(agent).sample(info["action_mask"])
        else:
            action = env.action_space(agent).sample()
        assert isinstance(terminated, bool), "terminated from last is not True or False"
        assert isinstance(truncated, bool), "terminated from last is not True or False"
        assert (
            terminated == env.terminations[agent]
        ), "terminated from last() and terminations[agent] do not match"
        assert (
            truncated == env.truncations[agent]
        ), "truncated from last() and truncations[agent] do not match"
        assert (
            info == env.infos[agent]
        ), "Info from last() and infos[agent] do not match"
        float(
            env.rewards[agent]
        )  # "Rewards for each agent must be convertible to float
        test_reward(reward)
        observation = env.step(action)
        assert observation is None, "step() must not return anything"

