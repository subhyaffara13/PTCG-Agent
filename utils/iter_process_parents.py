
def iter_process_parents(pid, max_depth=10):
    """Try to look up the process tree via the /proc interface."""
    stat_name = detect_proc()

    # Inner generator function so we correctly throw an error eagerly if proc
    # is not supported, rather than on the first call to the iterator. This
    # allows the call site detects the correct implementation.
    def _iter_process_parents(pid, max_depth):
        for _ in range(max_depth):
            ppid = _get_ppid(pid, stat_name)
            args = _get_cmdline(pid)
            yield Process(args=args, pid=pid, ppid=ppid)
            if ppid == "0":
                break
            pid = ppid

    return _iter_process_parents(pid, max_depth)


def iter_process_parents(pid, max_depth=10):
    """Try to look up the process tree via the output of `ps`."""
    try:
        cmd = ["ps", "-ww", "-o", "pid=", "-o", "ppid=", "-o", "args="]
        output = subprocess.check_output(cmd)
    except OSError as e:  # Python 2-compatible FileNotFoundError.
        if e.errno != errno.ENOENT:
            raise
        raise PsNotAvailable("ps not found")
    except subprocess.CalledProcessError as e:
        # `ps` can return 1 if the process list is completely empty.
        # (sarugaku/shellingham#15)
        if not e.output.strip():
            return
        raise
    if not isinstance(output, str):
        encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
        output = output.decode(encoding)

    processes_mapping = {}
    for line in output.split("\n"):
        try:
            _pid, ppid, args = line.strip().split(None, 2)
            # XXX: This is not right, but we are really out of options.
            # ps does not offer a sane way to decode the argument display,
            # and this is "Good Enough" for obtaining shell names. Hopefully
            # people don't name their shell with a space, or have something
            # like "/usr/bin/xonsh is uber". (sarugaku/shellingham#14)
            args = tuple(a.strip() for a in args.split(" "))
        except ValueError:
            continue
        processes_mapping[_pid] = Process(args=args, pid=_pid, ppid=ppid)

    for _ in range(max_depth):
        try:
            process = processes_mapping[pid]
        except KeyError:
            return
        yield process
        pid = process.ppid

