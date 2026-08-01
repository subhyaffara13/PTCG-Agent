
def _allow_interrupt_macos():
    """A context manager that allows terminating a plot by sending a SIGINT."""
    return _allow_interrupt(
        lambda rsock: _macosx.wake_on_fd_write(rsock.fileno()), _macosx.stop)

