
def _run_concurrent_barrier(n_workers, fn, *args, **kwargs):
    """
    Run a given function concurrently across a given number of threads.

    This function ensures that the closure passed by parameter gets called
    concurrently by setting up a barrier before it gets called before any of the
    threads.

    Returns a list of values returned by the worker threads.

    Arguments
    ---------
    n_workers: int
        Number of concurrent threads to spawn.
    fn: callable
        Function closure to execute concurrently. Its first argument will
        be the thread id.
    *args: tuple
        Variable number of positional arguments to pass to the function.
    **kwargs: dict
        Keyword arguments to pass to the function.

    """
    barrier = threading.Barrier(n_workers)

    def closure(i, *args, **kwargs):
        barrier.wait()
        return fn(i, *args, **kwargs)

    with ThreadPoolExecutor(max_workers=n_workers) as tpe:
        try:
            futures = []
            for i in range(0, n_workers):
                futures.append(tpe.submit(closure, i, *args, **kwargs))
        finally:
            if len(futures) < n_workers:
                # to avoid deadlocks if spawning failed for some reason
                barrier.abort()

    return [f.result() for f in futures]

