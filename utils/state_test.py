
def state_test(env, parallel_env, num_cycles=10):
    test_state_space(env)
    test_state(env, num_cycles)
    test_parallel_env(parallel_env)

