
def cpu_count_cores():
    cmd = ["lsdev", "-Cc", "processor"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    stdout, stderr = (x.decode(sys.stdout.encoding) for x in (stdout, stderr))
    if p.returncode != 0:
        msg = f"{cmd!r} command error\n{stderr}"
        raise RuntimeError(msg)
    processors = stdout.strip().splitlines()
    return len(processors) or None


def cpu_count_cores():
    """Return the number of CPU cores in the system."""
    # Method #1
    ls = set()
    # These 2 files are the same but */core_cpus_list is newer while
    # */thread_siblings_list is deprecated and may disappear in the future.
    # https://www.kernel.org/doc/Documentation/admin-guide/cputopology.rst
    # https://github.com/giampaolo/psutil/pull/1727#issuecomment-707624964
    # https://lkml.org/lkml/2019/2/26/41
    p1 = "/sys/devices/system/cpu/cpu[0-9]*/topology/core_cpus_list"
    p2 = "/sys/devices/system/cpu/cpu[0-9]*/topology/thread_siblings_list"
    for path in glob.glob(p1) or glob.glob(p2):
        with open_binary(path) as f:
            ls.add(f.read().strip())
    result = len(ls)
    if result != 0:
        return result

    # Method #2
    mapping = {}
    current_info = {}
    with open_binary(f"{get_procfs_path()}/cpuinfo") as f:
        for line in f:
            line = line.strip().lower()
            if not line:
                # new section
                try:
                    mapping[current_info[b'physical id']] = current_info[
                        b'cpu cores'
                    ]
                except KeyError:
                    pass
                current_info = {}
            elif line.startswith((b'physical id', b'cpu cores')):
                # ongoing section
                key, value = line.split(b'\t:', 1)
                current_info[key] = int(value)

    result = sum(mapping.values())
    return result or None  # mimic os.cpu_count()


def cpu_count_cores():
    """Return the number of CPU cores in the system."""
    return cext.cpu_count_cores()


def cpu_count_cores():
    """Return the number of CPU cores in the system."""
    return cext.cpu_count_cores()


def cpu_count_cores():
    """Return the number of CPU cores in the system."""
    return cext.cpu_count_cores()

