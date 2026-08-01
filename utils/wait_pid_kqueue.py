
def wait_pid_kqueue(pid, timeout=None):
    """Wait for PID to terminate using kqueue(). macOS and BSD only."""
    try:
        kq = select.kqueue()
    except OSError as err:
        if err.errno in {errno.EMFILE, errno.ENFILE}:  # too many open files
            debug(f"kqueue() failed ({err!r}); use fallback")
            return wait_pid_posix(pid, timeout)
        raise

    try:
        kev = select.kevent(
            pid,
            filter=select.KQ_FILTER_PROC,
            flags=select.KQ_EV_ADD | select.KQ_EV_ONESHOT,
            fflags=select.KQ_NOTE_EXIT,
        )
        try:
            events = kq.control([kev], 1, timeout)  # wait
        except OSError as err:
            if err.errno in {errno.EACCES, errno.EPERM, errno.ESRCH}:
                debug(f"kqueue.control() failed ({err!r}); use fallback")
                return wait_pid_posix(pid, timeout)
            raise
        else:
            if not events:
                raise TimeoutExpired(timeout)
            return _waitpid(pid, timeout)
    finally:
        kq.close()

