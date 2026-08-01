
def benchmark_render(env: gymnasium.Env, target_duration: int = 5) -> float:
    """A benchmark to measure the time of render().

    Note: does not work with `render_mode='human'`
    Args:
        env: the environment to benchmarked (Note: must be renderable).
        target_duration: the duration of the benchmark in seconds (note: it will go slightly over it).

    """
    renders = 0
    end = 0.0
    start = time.time()
    while True:
        renders += 1
        env.render()

        if time.time() - start > target_duration:
            end = time.time()
            break
    length = end - start

    renders_per_time = renders / length
    return renders_per_time

