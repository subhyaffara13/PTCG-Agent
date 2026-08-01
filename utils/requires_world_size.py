
def requires_world_size(n: int):
    """
    Decorator to request a specific world size for a test. The test harness can
    read this attribute to set the number of ranks to spawn. If there are fewer
    than `n` CUDA devices available, the test should be skipped by the harness.

    Usage:
        @require_world_size(3)
        def test_something(self):
            ...
    """

    def decorator(func):
        func._required_world_size = n
        available = torch.cuda.device_count()
        return unittest.skipUnless(
            available >= n, f"requires {n} GPUs, found {available}"
        )(func)

    return decorator

