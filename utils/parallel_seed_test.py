
def parallel_seed_test(parallel_env_fn):
    env1 = parallel_env_fn()
    env2 = parallel_env_fn()

    check_environment_deterministic_parallel(env1, env2, 500)

