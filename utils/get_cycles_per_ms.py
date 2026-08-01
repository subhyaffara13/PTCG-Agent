
def get_cycles_per_ms(device: str = "cuda") -> float:
    """Measure and return approximate number of cycles per millisecond for device _sleep.

    Args:
        device: Device type to measure cycles for ("cuda" or "cpu").

    Works for both CUDA (torch.cuda._sleep) and CPU (torch.cpu._sleep).
    """
    test_cycles = 1000000

    if device == "cpu":
        import time

        def measure() -> float:
            start = time.perf_counter()
            _cpu_sleep(test_cycles)
            end = time.perf_counter()
            elapsed_ms = (end - start) * 1000
            cycles_per_ms = test_cycles / elapsed_ms if elapsed_ms > 0 else 1000000
            return cycles_per_ms
    else:
        def measure() -> float:
            start = torch.cuda.Event(enable_timing=True)
            end = torch.cuda.Event(enable_timing=True)
            start.record()
            torch.cuda._sleep(test_cycles)
            end.record()
            end.synchronize()
            cycles_per_ms = test_cycles / start.elapsed_time(end)
            return cycles_per_ms

    # Get 10 values and remove the 2 max and 2 min and return the avg.
    # This is to avoid system disturbance that skew the results, e.g.
    # the very first cuda call likely does a bunch of init, which takes
    # much longer than subsequent calls.
    #
    # Tested on both Tesla V100, Quadro GP100, Titan RTX, RTX 3090 GPUs
    # and seems to return stable values. Therefore, we enable caching
    # using lru_cache decorator above.
    num = 10
    vals = [measure() for _ in range(num)]
    vals = sorted(vals)
    return mean(vals[2 : num - 2])

