
def get_shell(pid=None, max_depth=10):
    proc_map = {
        proc.th32ProcessID: (proc.th32ParentProcessID, proc.szExeFile)
        for proc in _iter_processes()
    }
    pid = pid or os.getpid()

    for _ in range(0, max_depth + 1):
        try:
            ppid, executable = proc_map[pid]
        except KeyError:  # No such process? Give up.
            break

        # The executable name would be encoded with the current code page if
        # we're in ANSI mode (usually). Try to decode it into str/unicode,
        # replacing invalid characters to be safe (not thoeratically necessary,
        # I think). Note that we need to use 'mbcs' instead of encoding
        # settings from sys because this is from the Windows API, not Python
        # internals (which those settings reflect). (pypa/pipenv#3382)
        if isinstance(executable, bytes):
            executable = executable.decode("mbcs", "replace")

        name = executable.rpartition(".")[0].lower()
        if name not in SHELL_NAMES:
            pid = ppid
            continue

        key = PROCESS_QUERY_LIMITED_INFORMATION
        with _handle(kernel32.OpenProcess, key, 0, pid) as proch:
            return (name, _get_full_path(proch))

    return None


def get_shell(pid=None, max_depth=10):
    """Get the shell that the supplied pid or os.getpid() is running in."""
    pid = str(pid or os.getpid())
    for proc_args, _, _ in _iter_process_parents(pid, max_depth):
        shell = _get_shell(*proc_args)
        if shell:
            return shell
    return None

