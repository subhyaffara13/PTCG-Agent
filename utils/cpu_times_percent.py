
def cpu_times_percent(interval=None, percpu=False):
    """Same as cpu_percent() but provides utilization percentages
    for each specific CPU time as is returned by cpu_times().
    For instance, on Linux we'll get:

      >>> cpu_times_percent()
      cpupercent(user=4.8, nice=0.0, system=4.8, idle=90.5, iowait=0.0,
                 irq=0.0, softirq=0.0, steal=0.0, guest=0.0, guest_nice=0.0)
      >>>

    *interval* and *percpu* arguments have the same meaning as in
    cpu_percent().
    """
    tid = threading.current_thread().ident
    blocking = interval is not None and interval > 0.0
    if interval is not None and interval < 0:
        msg = f"interval is not positive (got {interval!r})"
        raise ValueError(msg)

    def calculate(t1, t2):
        nums = []
        times_delta = _cpu_times_deltas(t1, t2)
        all_delta = _cpu_tot_time(times_delta)
        # "scale" is the value to multiply each delta with to get percentages.
        # We use "max" to avoid division by zero (if all_delta is 0, then all
        # fields are 0 so percentages will be 0 too. all_delta cannot be a
        # fraction because cpu times are integers)
        scale = 100.0 / max(1, all_delta)
        for field_delta in times_delta:
            field_perc = field_delta * scale
            field_perc = round(field_perc, 1)
            # make sure we don't return negative values or values over 100%
            field_perc = min(max(0.0, field_perc), 100.0)
            nums.append(field_perc)
        return _ntp.scputimes(*nums)

    # system-wide usage
    if not percpu:
        if blocking:
            t1 = cpu_times()
            time.sleep(interval)
        else:
            t1 = _last_cpu_times_2.get(tid) or cpu_times()
        _last_cpu_times_2[tid] = cpu_times()
        return calculate(t1, _last_cpu_times_2[tid])
    # per-cpu usage
    else:
        ret = []
        if blocking:
            tot1 = cpu_times(percpu=True)
            time.sleep(interval)
        else:
            tot1 = _last_per_cpu_times_2.get(tid) or cpu_times(percpu=True)
        _last_per_cpu_times_2[tid] = cpu_times(percpu=True)
        for t1, t2 in zip(tot1, _last_per_cpu_times_2[tid]):
            ret.append(calculate(t1, t2))
        return ret

