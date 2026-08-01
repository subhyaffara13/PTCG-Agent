
def time_spent_us(t0: int) -> int:
    return int((time.perf_counter_ns() - t0) / 1000)

