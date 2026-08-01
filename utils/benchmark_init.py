
def benchmark_init(
    env_lambda: Callable[[], gymnasium.Env], target_duration: int = 5, seed=None
) -> float:
    """A benchmark to measure the initialization time and first reset.

    Args:
        env_lambda: the function to initialize the environment.
        target_duration: the duration of the benchmark in seconds (note: it will go slightly over it).
        seed: seeds the first reset of the environment.
    """
    inits = 0
    end = 0.0
    start = time.time()
    while True:
        inits += 1
        env = env_lambda()
        env.reset(seed=seed)

        if time.time() - start > target_duration:
            end = time.time()
            break
    length = end - start

    inits_per_time = inits / length
    return inits_per_time

