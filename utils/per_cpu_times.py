
def per_cpu_times():
    """Return system per-CPU times as a list of named tuples."""
    ret = cext.per_cpu_times()
    return [ntp.scputimes(*x) for x in ret]


def per_cpu_times():
    """Return system CPU times as a namedtuple."""
    ret = []
    for cpu_t in cext.per_cpu_times():
        user, nice, system, idle, irq = cpu_t
        item = ntp.scputimes(user, nice, system, idle, irq)
        ret.append(item)
    return ret


def per_cpu_times():
    """Return a list of namedtuple representing the CPU times
    for every CPU available on the system.
    """
    procfs_path = get_procfs_path()
    cpus = []
    with open_binary(f"{procfs_path}/stat") as f:
        # get rid of the first line which refers to system wide CPU stats
        f.readline()
        for line in f:
            if line.startswith(b'cpu'):
                values = line.split()
                fields = values[1 : len(ntp.scputimes._fields) + 1]
                fields = [float(x) / CLOCK_TICKS for x in fields]
                entry = ntp.scputimes(*fields)
                cpus.append(entry)
        return cpus


def per_cpu_times():
    """Return system CPU times as a named tuple."""
    ret = []
    for cpu_t in cext.per_cpu_times():
        user, nice, system, idle = cpu_t
        item = ntp.scputimes(user, nice, system, idle)
        ret.append(item)
    return ret


def per_cpu_times():
    """Return system per-CPU times as a list of named tuples."""
    ret = cext.per_cpu_times()
    return [ntp.scputimes(*x) for x in ret]


def per_cpu_times():
    """Return system per-CPU times as a list of named tuples."""
    ret = []
    for user, system, idle, interrupt, dpc in cext.per_cpu_times():
        item = ntp.scputimes(user, system, idle, interrupt, dpc)
        ret.append(item)
    return ret

