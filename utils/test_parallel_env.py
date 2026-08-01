
def test_parallel_env(parallel_env):
    parallel_env.reset()

    assert isinstance(
        parallel_env.state_space, gymnasium.spaces.Space
    ), "State space for each parallel environment must extend gymnasium.spaces.Space"

    state_0 = parallel_env.state()
    assert parallel_env.state_space.contains(
        state_0
    ), "ParallelEnvironment's state is outside of it's state space"

