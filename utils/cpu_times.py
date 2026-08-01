
def cpu_times():
    """Return system-wide CPU times as a named tuple."""
    ret = cext.per_cpu_times()
    return ntp.scputimes(*[sum(x) for x in zip(*ret)])


def cpu_times():
    """Return system per-CPU times as a namedtuple."""
    user, nice, system, idle, irq = cext.cpu_times()
    return ntp.scputimes(user, nice, system, idle, irq)


def cpu_times():
    """Return a named tuple representing the following system-wide
    CPU times:
    (user, nice, system, idle, iowait, irq, softirq [steal, [guest,
     [guest_nice]]])
    Last 3 fields may not be available on all Linux kernel versions.
    """
    procfs_path = get_procfs_path()
    with open_binary(f"{procfs_path}/stat") as f:
        values = f.readline().split()
    fields = values[1 : len(ntp.scputimes._fields) + 1]
    fields = [float(x) / CLOCK_TICKS for x in fields]
    return ntp.scputimes(*fields)


def cpu_times():
    """Return system CPU times as a namedtuple."""
    user, nice, system, idle = cext.cpu_times()
    return ntp.scputimes(user, nice, system, idle)


def cpu_times():
    """Return system-wide CPU times as a named tuple."""
    ret = cext.per_cpu_times()
    return ntp.scputimes(*[sum(x) for x in zip(*ret)])


def cpu_times():
    """Return system CPU times as a named tuple."""
    user, system, idle = cext.cpu_times()
    # Internally, GetSystemTimes() is used, and it doesn't return
    # interrupt and dpc times. cext.per_cpu_times() does, so we
    # rely on it to get those only.
    percpu_summed = ntp.scputimes(
        *[sum(n) for n in zip(*cext.per_cpu_times())]
    )
    return ntp.scputimes(
        user, system, idle, percpu_summed.interrupt, percpu_summed.dpc
    )


def cpu_times(percpu=False):
    """Return system-wide CPU times as a namedtuple.
    Every CPU time represents the seconds the CPU has spent in the
    given mode. The namedtuple's fields availability varies depending on the
    platform:

     - user
     - system
     - idle
     - nice (UNIX)
     - iowait (Linux)
     - irq (Linux, FreeBSD)
     - softirq (Linux)
     - steal (Linux >= 2.6.11)
     - guest (Linux >= 2.6.24)
     - guest_nice (Linux >= 3.2.0)

    When *percpu* is True return a list of namedtuples for each CPU.
    First element of the list refers to first CPU, second element
    to second CPU and so on.
    The order of the list is consistent across calls.
    """
    if not percpu:
        return _psplatform.cpu_times()
    else:
        return _psplatform.per_cpu_times()

