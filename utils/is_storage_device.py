
def is_storage_device(name):
    """Return True if the given name refers to a root device (e.g.
    "sda", "nvme0n1") as opposed to a logical partition (e.g.  "sda1",
    "nvme0n1p1"). If name is a virtual device (e.g. "loop1", "ram")
    return True.
    """
    # Re-adapted from iostat source code, see:
    # https://github.com/sysstat/sysstat/blob/
    #     97912938cd476645b267280069e83b1c8dc0e1c7/common.c#L208
    # Some devices may have a slash in their name (e.g. cciss/c0d0...).
    name = name.replace('/', '!')
    including_virtual = True
    if including_virtual:
        path = f"/sys/block/{name}"
    else:
        path = f"/sys/block/{name}/device"
    return os.access(path, os.F_OK)

