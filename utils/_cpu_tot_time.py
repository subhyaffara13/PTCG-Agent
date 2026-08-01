
def _cpu_tot_time(times):
    """Given a cpu_time() ntuple calculates the total CPU time
    (including idle time).
    """
    tot = sum(times)
    if LINUX:
        # On Linux guest times are already accounted in "user" or
        # "nice" times, so we subtract them from total.
        # Htop does the same. References:
        # https://github.com/giampaolo/psutil/pull/940
        # http://unix.stackexchange.com/questions/178045
        # https://github.com/torvalds/linux/blob/
        #     447976ef4fd09b1be88b316d1a81553f1aa7cd07/kernel/sched/
        #     cputime.c#L158
        tot -= getattr(times, "guest", 0)  # Linux 2.6.24+
        tot -= getattr(times, "guest_nice", 0)  # Linux 3.2.0+
    return tot

