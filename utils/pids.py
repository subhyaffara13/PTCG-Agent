
def pids():
    """Returns a list of PIDs currently running on the system."""
    return [int(x) for x in os.listdir(get_procfs_path()) if x.isdigit()]


def pids():
    """Returns a list of PIDs currently running on the system."""
    ret = cext.pids()
    if OPENBSD and (0 not in ret) and _pid_0_exists():
        # On OpenBSD the kernel does not return PID 0 (neither does
        # ps) but it's actually querable (Process(0) will succeed).
        ret.insert(0, 0)
    return ret


def pids():
    """Returns a list of PIDs currently running on the system."""
    path = get_procfs_path().encode(ENCODING)
    return [int(x) for x in os.listdir(path) if x.isdigit()]


def pids():
    ls = cext.pids()
    if 0 not in ls:
        # On certain macOS versions pids() C doesn't return PID 0 but
        # "ps" does and the process is querable via sysctl():
        # https://travis-ci.org/giampaolo/psutil/jobs/309619941
        try:
            Process(0).create_time()
            ls.insert(0, 0)
        except NoSuchProcess:
            pass
        except AccessDenied:
            ls.insert(0, 0)
    return ls


def pids():
    """Returns a list of PIDs currently running on the system."""
    path = get_procfs_path().encode(ENCODING)
    return [int(x) for x in os.listdir(path) if x.isdigit()]


def pids():
    """Return a list of current running PIDs."""
    global _LOWEST_PID
    ret = sorted(_psplatform.pids())
    _LOWEST_PID = ret[0]
    return ret

