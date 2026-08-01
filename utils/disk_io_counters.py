
def disk_io_counters(perdisk=False):
    """Return disk I/O statistics for every disk installed on the
    system as a dict of raw tuples.
    """

    def read_procfs():
        # OK, this is a bit confusing. The format of /proc/diskstats can
        # have 3 variations.
        # On Linux 2.4 each line has always 15 fields, e.g.:
        # "3     0   8 hda 8 8 8 8 8 8 8 8 8 8 8"
        # On Linux 2.6+ each line *usually* has 14 fields, and the disk
        # name is in another position, like this:
        # "3    0   hda 8 8 8 8 8 8 8 8 8 8 8"
        # ...unless (Linux 2.6) the line refers to a partition instead
        # of a disk, in which case the line has less fields (7):
        # "3    1   hda1 8 8 8 8"
        # 4.18+ has 4 fields added:
        # "3    0   hda 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0"
        # 5.5 has 2 more fields.
        # See:
        # https://www.kernel.org/doc/Documentation/iostats.txt
        # https://www.kernel.org/doc/Documentation/ABI/testing/procfs-diskstats
        with open_text(f"{get_procfs_path()}/diskstats") as f:
            lines = f.readlines()
        for line in lines:
            fields = line.split()
            flen = len(fields)
            # fmt: off
            if flen == 15:
                # Linux 2.4
                name = fields[3]
                reads = int(fields[2])
                (reads_merged, rbytes, rtime, writes, writes_merged,
                    wbytes, wtime, _, busy_time, _) = map(int, fields[4:14])
            elif flen == 14 or flen >= 18:
                # Linux 2.6+, line referring to a disk
                name = fields[2]
                (reads, reads_merged, rbytes, rtime, writes, writes_merged,
                    wbytes, wtime, _, busy_time, _) = map(int, fields[3:14])
            elif flen == 7:
                # Linux 2.6+, line referring to a partition
                name = fields[2]
                reads, rbytes, writes, wbytes = map(int, fields[3:])
                rtime = wtime = reads_merged = writes_merged = busy_time = 0
            else:
                msg = f"not sure how to interpret line {line!r}"
                raise ValueError(msg)
            yield (name, reads, writes, rbytes, wbytes, rtime, wtime,
                   reads_merged, writes_merged, busy_time)
            # fmt: on

    def read_sysfs():
        for block in os.listdir('/sys/block'):
            for root, _, files in os.walk(os.path.join('/sys/block', block)):
                if 'stat' not in files:
                    continue
                with open_text(os.path.join(root, 'stat')) as f:
                    fields = f.read().strip().split()
                name = os.path.basename(root)
                # fmt: off
                (reads, reads_merged, rbytes, rtime, writes, writes_merged,
                    wbytes, wtime, _, busy_time) = map(int, fields[:10])
                yield (name, reads, writes, rbytes, wbytes, rtime,
                       wtime, reads_merged, writes_merged, busy_time)
                # fmt: on

    if os.path.exists(f"{get_procfs_path()}/diskstats"):
        gen = read_procfs()
    elif os.path.exists('/sys/block'):
        gen = read_sysfs()
    else:
        msg = (
            f"{get_procfs_path()}/diskstats nor /sys/block are available on"
            " this system"
        )
        raise NotImplementedError(msg)

    retdict = {}
    for entry in gen:
        # fmt: off
        (name, reads, writes, rbytes, wbytes, rtime, wtime, reads_merged,
            writes_merged, busy_time) = entry
        if not perdisk and not is_storage_device(name):
            # perdisk=False means we want to calculate totals so we skip
            # partitions (e.g. 'sda1', 'nvme0n1p1') and only include
            # base disk devices (e.g. 'sda', 'nvme0n1'). Base disks
            # include a total of all their partitions + some extra size
            # of their own:
            #     $ cat /proc/diskstats
            #     259       0 sda 10485760 ...
            #     259       1 sda1 5186039 ...
            #     259       1 sda2 5082039 ...
            # See:
            # https://github.com/giampaolo/psutil/pull/1313
            continue

        rbytes *= DISK_SECTOR_SIZE
        wbytes *= DISK_SECTOR_SIZE
        retdict[name] = (reads, writes, rbytes, wbytes, rtime, wtime,
                         reads_merged, writes_merged, busy_time)
        # fmt: on

    return retdict


def disk_io_counters(perdisk=False, nowrap=True):
    """Return system disk I/O statistics as a namedtuple including
    the following fields:

     - read_count:  number of reads
     - write_count: number of writes
     - read_bytes:  number of bytes read
     - write_bytes: number of bytes written
     - read_time:   time spent reading from disk (in ms)
     - write_time:  time spent writing to disk (in ms)

    Platform specific:

     - busy_time: (Linux, FreeBSD) time spent doing actual I/Os (in ms)
     - read_merged_count (Linux): number of merged reads
     - write_merged_count (Linux): number of merged writes

    If *perdisk* is True return the same information for every
    physical disk installed on the system as a dictionary
    with partition names as the keys and the namedtuple
    described above as the values.

    If *nowrap* is True it detects and adjust the numbers which overflow
    and wrap (restart from 0) and add "old value" to "new value" so that
    the returned numbers will always be increasing or remain the same,
    but never decrease.
    "disk_io_counters.cache_clear()" can be used to invalidate the
    cache.

    On recent Windows versions 'diskperf -y' command may need to be
    executed first otherwise this function won't find any disk.
    """
    kwargs = dict(perdisk=perdisk) if LINUX else {}
    rawdict = _psplatform.disk_io_counters(**kwargs)
    if not rawdict:
        return {} if perdisk else None
    if nowrap:
        rawdict = _wrap_numbers(rawdict, 'psutil.disk_io_counters')
    if perdisk:
        for disk, fields in rawdict.items():
            rawdict[disk] = _ntp.sdiskio(*fields)
        return rawdict
    else:
        return _ntp.sdiskio(*(sum(x) for x in zip(*rawdict.values())))

