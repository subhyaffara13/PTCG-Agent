import os

def virtual_memory():
    total, avail, free, _pinned, inuse = cext.virtual_mem()
    percent = usage_percent((total - avail), total, round_=1)
    return ntp.svmem(total, avail, percent, inuse, free)


def virtual_memory():
    mem = cext.virtual_mem()
    if NETBSD:
        total, free, active, inactive, wired, cached = mem
        # On NetBSD buffers and shared mem is determined via /proc.
        # The C ext set them to 0.
        with open('/proc/meminfo', 'rb') as f:
            for line in f:
                if line.startswith(b'Buffers:'):
                    buffers = int(line.split()[1]) * 1024
                elif line.startswith(b'MemShared:'):
                    shared = int(line.split()[1]) * 1024
        # Before avail was calculated as (inactive + cached + free),
        # same as zabbix, but it turned out it could exceed total (see
        # #2233), so zabbix seems to be wrong. Htop calculates it
        # differently, and the used value seem more realistic, so let's
        # match htop.
        # https://github.com/htop-dev/htop/blob/e7f447b/netbsd/NetBSDProcessList.c#L162
        # https://github.com/zabbix/zabbix/blob/af5e0f8/src/libs/zbxsysinfo/netbsd/memory.c#L135
        used = active + wired
        avail = total - used
    else:
        total, free, active, inactive, wired, cached, buffers, shared = mem
        # matches freebsd-memory CLI:
        # * https://people.freebsd.org/~rse/dist/freebsd-memory
        # * https://www.cyberciti.biz/files/scripts/freebsd-memory.pl.txt
        # matches zabbix:
        # * https://github.com/zabbix/zabbix/blob/af5e0f8/src/libs/zbxsysinfo/freebsd/memory.c#L143
        avail = inactive + cached + free
        used = active + wired + cached

    percent = usage_percent((total - avail), total, round_=1)
    return ntp.svmem(
        total,
        avail,
        percent,
        used,
        free,
        active,
        inactive,
        buffers,
        cached,
        shared,
        wired,
    )


def virtual_memory():
    """Report virtual memory stats.
    This implementation mimics procps-ng-3.3.12, aka "free" CLI tool:
    https://gitlab.com/procps-ng/procps/blob/
        24fd2605c51fccc375ab0287cec33aa767f06718/proc/sysinfo.c#L778-791
    The returned values are supposed to match both "free" and "vmstat -s"
    CLI tools.
    """
    missing_fields = []
    mems = {}
    with open_binary(f"{get_procfs_path()}/meminfo") as f:
        for line in f:
            fields = line.split()
            mems[fields[0]] = int(fields[1]) * 1024

    # /proc doc states that the available fields in /proc/meminfo vary
    # by architecture and compile options, but these 3 values are also
    # returned by sysinfo(2); as such we assume they are always there.
    total = mems[b'MemTotal:']
    free = mems[b'MemFree:']
    try:
        buffers = mems[b'Buffers:']
    except KeyError:
        # https://github.com/giampaolo/psutil/issues/1010
        buffers = 0
        missing_fields.append('buffers')
    try:
        cached = mems[b"Cached:"]
    except KeyError:
        cached = 0
        missing_fields.append('cached')
    else:
        # "free" cmdline utility sums reclaimable to cached.
        # Older versions of procps used to add slab memory instead.
        # This got changed in:
        # https://gitlab.com/procps-ng/procps/commit/
        #     05d751c4f076a2f0118b914c5e51cfbb4762ad8e
        cached += mems.get(b"SReclaimable:", 0)  # since kernel 2.6.19

    try:
        shared = mems[b'Shmem:']  # since kernel 2.6.32
    except KeyError:
        try:
            shared = mems[b'MemShared:']  # kernels 2.4
        except KeyError:
            shared = 0
            missing_fields.append('shared')

    try:
        active = mems[b"Active:"]
    except KeyError:
        active = 0
        missing_fields.append('active')

    try:
        inactive = mems[b"Inactive:"]
    except KeyError:
        try:
            inactive = (
                mems[b"Inact_dirty:"]
                + mems[b"Inact_clean:"]
                + mems[b"Inact_laundry:"]
            )
        except KeyError:
            inactive = 0
            missing_fields.append('inactive')

    try:
        slab = mems[b"Slab:"]
    except KeyError:
        slab = 0

    # - starting from 4.4.0 we match free's "available" column.
    #   Before 4.4.0 we calculated it as (free + buffers + cached)
    #   which matched htop.
    # - free and htop available memory differs as per:
    #   http://askubuntu.com/a/369589
    #   http://unix.stackexchange.com/a/65852/168884
    # - MemAvailable has been introduced in kernel 3.14
    try:
        avail = mems[b'MemAvailable:']
    except KeyError:
        avail = calculate_avail_vmem(mems)
    else:
        if avail == 0:
            # Yes, it can happen (probably a kernel bug):
            # https://github.com/giampaolo/psutil/issues/1915
            # In this case "free" CLI tool makes an estimate. We do the same,
            # and it matches "free" CLI tool.
            avail = calculate_avail_vmem(mems)

    if avail < 0:
        avail = 0
        missing_fields.append('available')
    elif avail > total:
        # If avail is greater than total or our calculation overflows,
        # that's symptomatic of running within a LCX container where such
        # values will be dramatically distorted over those of the host.
        # https://gitlab.com/procps-ng/procps/blob/
        #     24fd2605c51fccc375ab0287cec33aa767f06718/proc/sysinfo.c#L764
        avail = free

    used = total - avail

    percent = usage_percent((total - avail), total, round_=1)

    # Warn about missing metrics which are set to 0.
    if missing_fields:
        msg = "{} memory stats couldn't be determined and {} set to 0".format(
            ", ".join(missing_fields),
            "was" if len(missing_fields) == 1 else "were",
        )
        warnings.warn(msg, RuntimeWarning, stacklevel=2)

    return ntp.svmem(
        total,
        avail,
        percent,
        used,
        free,
        active,
        inactive,
        buffers,
        cached,
        shared,
        slab,
    )


def virtual_memory():
    """System virtual memory as a namedtuple."""
    total, active, inactive, wired, free, speculative = cext.virtual_mem()
    # This is how Zabbix calculate avail and used mem:
    # https://github.com/zabbix/zabbix/blob/master/src/libs/zbxsysinfo/osx/memory.c
    # Also see: https://github.com/giampaolo/psutil/issues/1277
    avail = inactive + free
    used = active + wired
    # This is NOT how Zabbix calculates free mem but it matches "free"
    # cmdline utility.
    free -= speculative
    percent = usage_percent((total - avail), total, round_=1)
    return ntp.svmem(
        total, avail, percent, used, free, active, inactive, wired
    )


def virtual_memory():
    """Report virtual memory metrics."""
    # we could have done this with kstat, but IMHO this is good enough
    total = os.sysconf('SC_PHYS_PAGES') * PAGE_SIZE
    # note: there's no difference on Solaris
    free = avail = os.sysconf('SC_AVPHYS_PAGES') * PAGE_SIZE
    used = total - free
    percent = usage_percent(used, total, round_=1)
    return ntp.svmem(total, avail, percent, used, free)


def virtual_memory():
    """System virtual memory as a namedtuple."""
    mem = cext.virtual_mem()
    totphys, availphys, _totsys, _availsys = mem
    total = totphys
    avail = availphys
    free = availphys
    used = total - avail
    percent = usage_percent((total - avail), total, round_=1)
    return ntp.svmem(total, avail, percent, used, free)


def virtual_memory():
    """Return statistics about system memory usage as a namedtuple
    including the following fields, expressed in bytes:

     - total:
       total physical memory available.

     - available:
       the memory that can be given instantly to processes without the
       system going into swap.
       This is calculated by summing different memory values depending
       on the platform and it is supposed to be used to monitor actual
       memory usage in a cross platform fashion.

     - percent:
       the percentage usage calculated as (total - available) / total * 100

     - used:
        memory used, calculated differently depending on the platform and
        designed for informational purposes only:
        macOS: active + wired
        BSD: active + wired + cached
        Linux: total - free

     - free:
       memory not being used at all (zeroed) that is readily available;
       note that this doesn't reflect the actual memory available
       (use 'available' instead)

    Platform-specific fields:

     - active (UNIX):
       memory currently in use or very recently used, and so it is in RAM.

     - inactive (UNIX):
       memory that is marked as not used.

     - buffers (BSD, Linux):
       cache for things like file system metadata.

     - cached (BSD, macOS):
       cache for various things.

     - wired (macOS, BSD):
       memory that is marked to always stay in RAM. It is never moved to disk.

     - shared (BSD):
       memory that may be simultaneously accessed by multiple processes.

    The sum of 'used' and 'available' does not necessarily equal total.
    On Windows 'available' and 'free' are the same.
    """
    global _TOTAL_PHYMEM
    ret = _psplatform.virtual_memory()
    # cached for later use in Process.memory_percent()
    _TOTAL_PHYMEM = ret.total
    return ret

