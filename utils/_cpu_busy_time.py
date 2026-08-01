
def _cpu_busy_time(times):
    """Given a cpu_time() ntuple calculates the busy CPU time.
    We do so by subtracting all idle CPU times.
    """
    busy = _cpu_tot_time(times)
    busy -= times.idle
    # Linux: "iowait" is time during which the CPU does not do anything
    # (waits for IO to complete). On Linux IO wait is *not* accounted
    # in "idle" time so we subtract it. Htop does the same.
    # References:
    # https://github.com/torvalds/linux/blob/
    #     447976ef4fd09b1be88b316d1a81553f1aa7cd07/kernel/sched/cputime.c#L244
    busy -= getattr(times, "iowait", 0)
    return busy

