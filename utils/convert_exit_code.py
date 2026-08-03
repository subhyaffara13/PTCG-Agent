import os

def convert_exit_code(status):
    """Convert a os.waitpid() status to an exit code."""
    if os.WIFEXITED(status):
        # Process terminated normally by calling exit(3) or _exit(2),
        # or by returning from main(). The return value is the
        # positive integer passed to *exit().
        return os.WEXITSTATUS(status)
    if os.WIFSIGNALED(status):
        # Process exited due to a signal. Return the negative value
        # of that signal.
        return negsig_to_enum(-os.WTERMSIG(status))
    # if os.WIFSTOPPED(status):
    #     # Process was stopped via SIGSTOP or is being traced, and
    #     # waitpid() was called with WUNTRACED flag. PID is still
    #     # alive. From now on waitpid() will keep returning (0, 0)
    #     # until the process state doesn't change.
    #     # It may make sense to catch/enable this since stopped PIDs
    #     # ignore SIGTERM.
    #     interval = sleep(interval)
    #     continue
    # if os.WIFCONTINUED(status):
    #     # Process was resumed via SIGCONT and waitpid() was called
    #     # with WCONTINUED flag.
    #     interval = sleep(interval)
    #     continue

    # Should never happen.
    msg = f"unknown process exit status {status!r}"
    raise ValueError(msg)

