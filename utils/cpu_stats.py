
def cpu_stats():
    """Return various CPU stats as a named tuple."""
    ctx_switches, interrupts, soft_interrupts, syscalls = cext.cpu_stats()
    return ntp.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    if FREEBSD:
        # Note: the C ext is returning some metrics we are not exposing:
        # traps.
        ctxsw, intrs, soft_intrs, syscalls, _traps = cext.cpu_stats()
    elif NETBSD:
        # XXX
        # Note about intrs: the C extension returns 0. intrs
        # can be determined via /proc/stat; it has the same value as
        # soft_intrs thought so the kernel is faking it (?).
        #
        # Note about syscalls: the C extension always sets it to 0 (?).
        #
        # Note: the C ext is returning some metrics we are not exposing:
        # traps, faults and forks.
        ctxsw, intrs, soft_intrs, syscalls, _traps, _faults, _forks = (
            cext.cpu_stats()
        )
        with open('/proc/stat', 'rb') as f:
            for line in f:
                if line.startswith(b'intr'):
                    intrs = int(line.split()[1])
    elif OPENBSD:
        # Note: the C ext is returning some metrics we are not exposing:
        # traps, faults and forks.
        ctxsw, intrs, soft_intrs, syscalls, _traps, _faults, _forks = (
            cext.cpu_stats()
        )
    return ntp.scpustats(ctxsw, intrs, soft_intrs, syscalls)


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    with open_binary(f"{get_procfs_path()}/stat") as f:
        ctx_switches = None
        interrupts = None
        soft_interrupts = None
        for line in f:
            if line.startswith(b'ctxt'):
                ctx_switches = int(line.split()[1])
            elif line.startswith(b'intr'):
                interrupts = int(line.split()[1])
            elif line.startswith(b'softirq'):
                soft_interrupts = int(line.split()[1])
            if (
                ctx_switches is not None
                and soft_interrupts is not None
                and interrupts is not None
            ):
                break
    syscalls = 0
    return ntp.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_stats():
    ctx_switches, interrupts, soft_interrupts, syscalls, _traps = (
        cext.cpu_stats()
    )
    return ntp.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_stats():
    """Return various CPU stats as a named tuple."""
    ctx_switches, interrupts, syscalls, _traps = cext.cpu_stats()
    soft_interrupts = 0
    return ntp.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_stats():
    """Return CPU statistics."""
    ctx_switches, interrupts, _dpcs, syscalls = cext.cpu_stats()
    soft_interrupts = 0
    return ntp.scpustats(ctx_switches, interrupts, soft_interrupts, syscalls)


def cpu_stats():
    """Return CPU statistics."""
    return _psplatform.cpu_stats()

