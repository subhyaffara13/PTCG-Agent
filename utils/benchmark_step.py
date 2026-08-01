
def benchmark_step(env: gymnasium.Env, target_duration: int = 5, seed=None) -> float:
    """A benchmark to measure the runtime performance of step for an environment.

    example usage:
        ```py
        env_old = ...
        old_throughput = benchmark_step(env_old)
        env_new = ...
        new_throughput = benchmark_step(env_old)
        slowdown = old_throughput / new_throughput
        ```

    Args:
        env: the environment to benchmarked.
        target_duration: the duration of the benchmark in seconds (note: it will go slightly over it).
        seed: seeds the environment and action sampled.

    Returns: the average steps per second.
    """
    steps = 0
    end = 0.0
    env.reset(seed=seed)
    env.action_space.sample()
    start = time.time()

    while True:
        steps += 1
        action = env.action_space.sample()
        _, _, terminal, truncated, _ = env.step(action)

        if terminal or truncated:
            env.reset()

        if time.time() - start > target_duration:
            end = time.time()
            break

    length = end - start

    steps_per_time = steps / length
    return steps_per_time

