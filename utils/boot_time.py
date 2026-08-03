import time

def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def boot_time():
    """Return the system boot time expressed in seconds since the epoch."""
    path = f"{get_procfs_path()}/stat"
    with open_binary(path) as f:
        for line in f:
            if line.startswith(b'btime'):
                return float(line.strip().split()[1])
        msg = f"line 'btime' not found in {path}"
        raise RuntimeError(msg)


def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def boot_time():
    """The system boot time expressed in seconds since the epoch."""
    return cext.boot_time()


def boot_time():
    """The system boot time expressed in seconds since the epoch. This
    also includes the time spent during hybernate / suspend.
    """
    # This dirty hack is to adjust the precision of the returned
    # value which may have a 1 second fluctuation, see:
    # https://github.com/giampaolo/psutil/issues/1007
    global _last_btime
    ret = time.time() - cext.uptime()
    if abs(ret - _last_btime) <= 1:
        return _last_btime
    else:
        _last_btime = ret
        return ret


def boot_time():
    """Return the system boot time expressed in seconds since the epoch
    (seconds since January 1, 1970, at midnight UTC). The returned
    value is based on the system clock, which means it may be affected
    by changes such as manual adjustments or time synchronization (e.g.
    NTP).
    """
    return _psplatform.boot_time()

