import os

def disk_partitions(all=False):
    """Return system disk partitions."""
    # TODO - the filtering logic should be better checked so that
    # it tries to reflect 'df' as much as possible
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            # Differently from, say, Linux, we don't have a list of
            # common fs types so the best we can do, AFAIK, is to
            # filter by filesystem having a total size > 0.
            if not disk_usage(mountpoint).total:
                continue
        ntuple = ntp.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)
    return retlist


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples.
    'all' argument is ignored, see:
    https://github.com/giampaolo/psutil/issues/906.
    """
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        ntuple = ntp.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)
    return retlist


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples."""
    fstypes = set()
    procfs_path = get_procfs_path()
    if not all:
        with open_text(f"{procfs_path}/filesystems") as f:
            for line in f:
                line = line.strip()
                if not line.startswith("nodev"):
                    fstypes.add(line.strip())
                else:
                    # ignore all lines starting with "nodev" except "nodev zfs"
                    fstype = line.split("\t")[1]
                    if fstype == "zfs":
                        fstypes.add("zfs")

    # See: https://github.com/giampaolo/psutil/issues/1307
    if procfs_path == "/proc" and os.path.isfile('/etc/mtab'):
        mounts_path = os.path.realpath("/etc/mtab")
    else:
        mounts_path = os.path.realpath(f"{procfs_path}/self/mounts")

    retlist = []
    partitions = cext.disk_partitions(mounts_path)
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if device in {"/dev/root", "rootfs"}:
            device = RootFsDeviceFinder().find() or device
        if not all:
            if not device or fstype not in fstypes:
                continue
        ntuple = ntp.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)

    return retlist


def disk_partitions(all=False):
    """Return mounted disk partitions as a list of namedtuples."""
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            if not os.path.isabs(device) or not os.path.exists(device):
                continue
        ntuple = ntp.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)
    return retlist


def disk_partitions(all=False):
    """Return system disk partitions."""
    # TODO - the filtering logic should be better checked so that
    # it tries to reflect 'df' as much as possible
    retlist = []
    partitions = cext.disk_partitions()
    for partition in partitions:
        device, mountpoint, fstype, opts = partition
        if device == 'none':
            device = ''
        if not all:
            # Differently from, say, Linux, we don't have a list of
            # common fs types so the best we can do, AFAIK, is to
            # filter by filesystem having a total size > 0.
            try:
                if not disk_usage(mountpoint).total:
                    continue
            except OSError as err:
                # https://github.com/giampaolo/psutil/issues/1674
                debug(f"skipping {mountpoint!r}: {err}")
                continue
        ntuple = ntp.sdiskpart(device, mountpoint, fstype, opts)
        retlist.append(ntuple)
    return retlist


def disk_partitions(all):
    """Return disk partitions."""
    rawlist = cext.disk_partitions(all)
    return [ntp.sdiskpart(*x) for x in rawlist]


def disk_partitions(all=False):
    """Return mounted partitions as a list of
    (device, mountpoint, fstype, opts) namedtuple.
    'opts' field is a raw string separated by commas indicating mount
    options which may vary depending on the platform.

    If *all* parameter is False return physical devices only and ignore
    all others.
    """
    return _psplatform.disk_partitions(all)

