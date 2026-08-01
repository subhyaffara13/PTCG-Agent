
def wait_pid(pid, timeout=None):
    # PID 0 passed to waitpid() waits for any child of the current
    # process to change state.
    assert pid > 0
    if timeout is not None:
        assert timeout >= 0

    if can_use_pidfd_open():
        return wait_pid_pidfd_open(pid, timeout)
    elif can_use_kqueue():
        return wait_pid_kqueue(pid, timeout)
    else:
        return wait_pid_posix(pid, timeout)

