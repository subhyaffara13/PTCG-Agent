import os
import time

def wait_pid_posix(
    pid,
    timeout=None,
    _waitpid=os.waitpid,
    _timer=getattr(time, 'monotonic', time.time),  # noqa: B008
    _min=min,
    _sleep=time.sleep,
    _pid_exists=pid_exists,
):
    """Wait for a process PID to terminate.

    If the process terminated normally by calling exit(3) or _exit(2),
    or by returning from main(), the return value is the positive integer
    passed to *exit().

    If it was terminated by a signal it returns the negated value of the
    signal which caused the termination (e.g. -SIGTERM).

    If PID is not a children of os.getpid() (current process) just
    wait until the process disappears and return None.

    If PID does not exist at all return None immediately.

    If timeout is specified and process is still alive raise
    TimeoutExpired.

    If timeout=0 either return immediately or raise TimeoutExpired
    (non-blocking).
    """
    interval = 0.0001
    max_interval = 0.04
    flags = 0
    stop_at = None

    if timeout is not None:
        flags |= os.WNOHANG
        if timeout != 0:
            stop_at = _timer() + timeout

    def sleep_or_timeout(interval):
        # Sleep for some time and return a new increased interval.
        if timeout == 0 or (stop_at is not None and _timer() >= stop_at):
            raise TimeoutExpired(timeout)
        _sleep(interval)
        return _min(interval * 2, max_interval)

    # See: https://linux.die.net/man/2/waitpid
    while True:
        try:
            retpid, status = os.waitpid(pid, flags)
        except ChildProcessError:
            # This has two meanings:
            # - PID is not a child of os.getpid() in which case
            #   we keep polling until it's gone
            # - PID never existed in the first place
            # In both cases we'll eventually return None as we
            # can't determine its exit status code.
            while _pid_exists(pid):
                interval = sleep_or_timeout(interval)
            return None
        else:
            if retpid == 0:
                # WNOHANG flag was used and PID is still running.
                interval = sleep_or_timeout(interval)
            else:
                return convert_exit_code(status)

