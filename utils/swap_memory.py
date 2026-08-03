import os
import subprocess
import sys

def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""
    total, free, sin, sout = cext.swap_mem()
    used = total - free
    percent = usage_percent(used, total, round_=1)
    return ntp.sswap(total, used, free, percent, sin, sout)


def swap_memory():
    """System swap memory as (total, used, free, sin, sout) namedtuple."""
    total, used, free, sin, sout = cext.swap_mem()
    percent = usage_percent(used, total, round_=1)
    return ntp.sswap(total, used, free, percent, sin, sout)


def swap_memory():
    """Return swap memory metrics."""
    mems = {}
    with open_binary(f"{get_procfs_path()}/meminfo") as f:
        for line in f:
            fields = line.split()
            mems[fields[0]] = int(fields[1]) * 1024
    # We prefer /proc/meminfo over sysinfo() syscall so that
    # psutil.PROCFS_PATH can be used in order to allow retrieval
    # for linux containers, see:
    # https://github.com/giampaolo/psutil/issues/1015
    try:
        total = mems[b'SwapTotal:']
        free = mems[b'SwapFree:']
    except KeyError:
        _, _, _, _, total, free, unit_multiplier = cext.linux_sysinfo()
        total *= unit_multiplier
        free *= unit_multiplier

    used = total - free
    percent = usage_percent(used, total, round_=1)
    # get pgin/pgouts
    try:
        f = open_binary(f"{get_procfs_path()}/vmstat")
    except OSError as err:
        # see https://github.com/giampaolo/psutil/issues/722
        msg = (
            "'sin' and 'sout' swap memory stats couldn't "
            f"be determined and were set to 0 ({err})"
        )
        warnings.warn(msg, RuntimeWarning, stacklevel=2)
        sin = sout = 0
    else:
        with f:
            sin = sout = None
            for line in f:
                # values are expressed in 4 kilo bytes, we want
                # bytes instead
                if line.startswith(b'pswpin'):
                    sin = int(line.split(b' ')[1]) * 4 * 1024
                elif line.startswith(b'pswpout'):
                    sout = int(line.split(b' ')[1]) * 4 * 1024
                if sin is not None and sout is not None:
                    break
            else:
                # we might get here when dealing with exotic Linux
                # flavors, see:
                # https://github.com/giampaolo/psutil/issues/313
                msg = "'sin' and 'sout' swap memory stats couldn't "
                msg += "be determined and were set to 0"
                warnings.warn(msg, RuntimeWarning, stacklevel=2)
                sin = sout = 0
    return ntp.sswap(total, used, free, percent, sin, sout)


def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""
    total, used, free, sin, sout = cext.swap_mem()
    percent = usage_percent(used, total, round_=1)
    return ntp.sswap(total, used, free, percent, sin, sout)


def swap_memory():
    """Report swap memory metrics."""
    sin, sout = cext.swap_mem()
    # XXX
    # we are supposed to get total/free by doing so:
    # http://cvs.opensolaris.org/source/xref/onnv/onnv-gate/
    #     usr/src/cmd/swap/swap.c
    # ...nevertheless I can't manage to obtain the same numbers as 'swap'
    # cmdline utility, so let's parse its output (sigh!)
    p = subprocess.Popen(
        [
            '/usr/bin/env',
            f"PATH=/usr/sbin:/sbin:{os.environ['PATH']}",
            'swap',
            '-l',
        ],
        stdout=subprocess.PIPE,
    )
    stdout, _ = p.communicate()
    stdout = stdout.decode(sys.stdout.encoding)
    if p.returncode != 0:
        msg = f"'swap -l' failed (retcode={p.returncode})"
        raise RuntimeError(msg)

    lines = stdout.strip().split('\n')[1:]
    if not lines:
        msg = 'no swap device(s) configured'
        raise RuntimeError(msg)
    total = free = 0
    for line in lines:
        line = line.split()
        t, f = line[3:5]
        total += int(int(t) * 512)
        free += int(int(f) * 512)
    used = total - free
    percent = usage_percent(used, total, round_=1)
    return ntp.sswap(
        total, used, free, percent, sin * PAGE_SIZE, sout * PAGE_SIZE
    )


def swap_memory():
    """Swap system memory as a (total, used, free, sin, sout) tuple."""
    mem = cext.virtual_mem()

    total_phys = mem[0]
    total_system = mem[2]

    # system memory (commit total/limit) is the sum of physical and swap
    # thus physical memory values need to be subtracted to get swap values
    total = total_system - total_phys
    # commit total is incremented immediately (decrementing free_system)
    # while the corresponding free physical value is not decremented until
    # pages are accessed, so we can't use free system memory for swap.
    # instead, we calculate page file usage based on performance counter
    if total > 0:
        percentswap = cext.swap_percent()
        used = int(0.01 * percentswap * total)
    else:
        percentswap = 0.0
        used = 0

    free = total - used
    percent = round(percentswap, 1)
    return ntp.sswap(total, used, free, percent, 0, 0)


def swap_memory():
    """Return system swap memory statistics as a namedtuple including
    the following fields:

     - total:   total swap memory in bytes
     - used:    used swap memory in bytes
     - free:    free swap memory in bytes
     - percent: the percentage usage
     - sin:     no. of bytes the system has swapped in from disk (cumulative)
     - sout:    no. of bytes the system has swapped out from disk (cumulative)

    'sin' and 'sout' on Windows are meaningless and always set to 0.
    """
    return _psplatform.swap_memory()

