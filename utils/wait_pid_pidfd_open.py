import os

def wait_pid_pidfd_open(pid, timeout=None):
    """Wait for PID to terminate using pidfd_open() + poll(). Linux >=
    5.3 + Python >= 3.9 only.
    """
    try:
        pidfd = os.pidfd_open(pid, 0)
    except OSError as err:
        if err.errno == errno.ESRCH:
            # No such process. os.waitpid() may still be able to return
            # the status code.
            return wait_pid_posix(pid, timeout)
        if err.errno in {errno.EMFILE, errno.ENFILE, errno.ENODEV}:
            # EMFILE, ENFILE: too many open files
            # ENODEV: anonymous inode filesystem not supported
            debug(f"pidfd_open() failed ({err!r}); use fallback")
            return wait_pid_posix(pid, timeout)
        raise

    try:
        # poll() / select() have the advantage of not requiring any
        # extra file descriptor, contrary to epoll() / kqueue().
        # select() crashes if process opens > 1024 FDs, so we use
        # poll().
        poller = select.poll()
        poller.register(pidfd, select.POLLIN)
        timeout_ms = None if timeout is None else int(timeout * 1000)
        events = poller.poll(timeout_ms)  # wait

        if not events:
            raise TimeoutExpired(timeout)
        return _waitpid(pid, timeout)
    finally:
        os.close(pidfd)

