
def api_test(env, num_cycles=1000, verbose_progress=False):
    def progress_report(msg):
        if verbose_progress:
            print(msg)

    print("Starting API test")
    if not hasattr(env, "possible_agents"):
        warnings.warn(missing_attr_warning.format(name="possible_agents"))

    # checks that reset takes arguments called seed and options
    env.reset(seed=0, options={"options": 1})

    assert isinstance(
        env, pettingzoo.AECEnv
    ), "Env must be an instance of pettingzoo.AECEnv"

    env.reset()
    assert not any(
        env.terminations.values()
    ), "terminations must all be False after reset"
    assert not any(
        env.truncations.values()
    ), "truncations must all be False after reset"

    assert isinstance(env.num_agents, int), "num_agents must be an integer"
    assert env.num_agents != 0, "An environment should have a nonzero number of agents"
    assert env.num_agents > 0, "An environment should have a positive number of agents"

    env.reset()
    observation_0, *_ = env.last()
    if isinstance(observation_0, dict) and "observation" in observation_0:
        observation_0 = observation_0["observation"]

    test_observation(observation_0, observation_0, str(env.unwrapped))

    non_observe, *_ = env.last(observe=False)
    assert non_observe is None, "last must return a None when observe=False"

    progress_report("Finished test_observation")

    agent_0 = env.agent_selection

    test_observation_action_spaces(env, agent_0)

    progress_report("Finished test_observation_action_spaces")

    play_test(env, observation_0, num_cycles)

    progress_report("Finished play test")

    assert isinstance(env.rewards, dict), "rewards must be a dict"
    assert isinstance(env.terminations, dict), "terminations must be a dict"
    assert isinstance(env.truncations, dict), "truncations must be a dict"
    assert isinstance(env.infos, dict), "infos must be a dict"

    assert (
        len(env.rewards)
        == len(env.terminations)
        == len(env.truncations)
        == len(env.infos)
        == len(env.agents)
    ), "rewards, terminations, truncations, infos and agents must have the same length"

    test_rewards_terminations_truncations(env, agent_0)

    test_action_flexibility(env)

    progress_report("Finished test_rewards_terminations_truncations")

    # checks unwrapped attribute
    assert not isinstance(env.unwrapped, aec_to_parallel_wrapper)
    assert not isinstance(env.unwrapped, parallel_to_aec_wrapper)
    assert not isinstance(env.unwrapped, BaseWrapper)

    # Test that if env has overridden render(), they must have overridden close() as well
    base_render = pettingzoo.utils.env.AECEnv.render
    base_close = pettingzoo.utils.env.AECEnv.close
    if base_render != env.__class__.render:
        assert (
            base_close != env.__class__.close
        ), "If render method defined, then close method required"
    else:
        warnings.warn("Environment has not defined a render() method")

    print("Passed API test")

