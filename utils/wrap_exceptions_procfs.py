
def wrap_exceptions_procfs(inst):
    """Same as above, for routines relying on reading /proc fs."""
    pid, name, ppid = inst.pid, inst._name, inst._ppid
    try:
        yield
    except (ProcessLookupError, FileNotFoundError) as err:
        # ENOENT (no such file or directory) gets raised on open().
        # ESRCH (no such process) can get raised on read() if
        # process is gone in meantime.
        if cext.proc_is_zombie(inst.pid):
            raise ZombieProcess(pid, name, ppid) from err
        else:
            raise NoSuchProcess(pid, name) from err
    except PermissionError as err:
        raise AccessDenied(pid, name) from err

