import os

def _waitpid(pid, timeout):
    """Wrapper around os.waitpid(). PID is supposed to be gone already,
    it just returns the exit code.
    """
    try:
        retpid, status = os.waitpid(pid, 0)
    except ChildProcessError:
        # PID is not a child of os.getpid().
        return wait_pid_posix(pid, timeout)
    else:
        assert retpid != 0
        return convert_exit_code(status)

