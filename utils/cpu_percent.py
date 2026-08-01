
def cpu_percent(interval=None, percpu=False):
    """Return a float representing the current system-wide CPU
    utilization as a percentage.

    When *interval* is > 0.0 compares system CPU times elapsed before
    and after the interval (blocking).

    When *interval* is 0.0 or None compares system CPU times elapsed
    since last call or module import, returning immediately (non
    blocking). That means the first time this is called it will
    return a meaningless 0.0 value which you should ignore.
    In this case is recommended for accuracy that this function be
    called with at least 0.1 seconds between calls.

    When *percpu* is True returns a list of floats representing the
    utilization as a percentage for each CPU.
    First element of the list refers to first CPU, second element
    to second CPU and so on.
    The order of the list is consistent across calls.

    Examples:

      >>> # blocking, system-wide
      >>> psutil.cpu_percent(interval=1)
      2.0
      >>>
      >>> # blocking, per-cpu
      >>> psutil.cpu_percent(interval=1, percpu=True)
      [2.0, 1.0]
      >>>
      >>> # non-blocking (percentage since last call)
      >>> psutil.cpu_percent(interval=None)
      2.9
      >>>
    """
    tid = threading.current_thread().ident
    blocking = interval is not None and interval > 0.0
    if interval is not None and interval < 0:
        msg = f"interval is not positive (got {interval})"
        raise ValueError(msg)

    def calculate(t1, t2):
        times_delta = _cpu_times_deltas(t1, t2)
        all_delta = _cpu_tot_time(times_delta)
        busy_delta = _cpu_busy_time(times_delta)

        try:
            busy_perc = (busy_delta / all_delta) * 100
        except ZeroDivisionError:
            return 0.0
        else:
            return round(busy_perc, 1)

    # system-wide usage
    if not percpu:
        if blocking:
            t1 = cpu_times()
            time.sleep(interval)
        else:
            t1 = _last_cpu_times.get(tid) or cpu_times()
        _last_cpu_times[tid] = cpu_times()
        return calculate(t1, _last_cpu_times[tid])
    # per-cpu usage
    else:
        ret = []
        if blocking:
            tot1 = cpu_times(percpu=True)
            time.sleep(interval)
        else:
            tot1 = _last_per_cpu_times.get(tid) or cpu_times(percpu=True)
        _last_per_cpu_times[tid] = cpu_times(percpu=True)
        for t1, t2 in zip(tot1, _last_per_cpu_times[tid]):
            ret.append(calculate(t1, t2))
        return ret

