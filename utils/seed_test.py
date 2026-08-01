
def seed_test(env_constructor, num_cycles=10):
    env1 = env_constructor()
    env2 = env_constructor()

    check_environment_deterministic(env1, env2, 500)

