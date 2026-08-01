
def test_parallel_randomstate():
    # if the coercion cache is enabled and not thread-safe, creating
    # RandomState instances simultaneously leads to a data race
    def func(seed):
        np.random.RandomState(seed)

    run_threaded(func, 500, pass_count=True)

    # seeding and setting state shouldn't race with generating RNG samples
    rng = np.random.RandomState()

    def func(seed):
        base_rng = np.random.RandomState(seed)
        state = base_rng.get_state()
        rng.seed(seed)
        rng.random()
        rng.set_state(state)

    run_threaded(func, 8, pass_count=True)

