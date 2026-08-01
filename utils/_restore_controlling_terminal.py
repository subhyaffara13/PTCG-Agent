
def _restore_controlling_terminal() -> None:
    """Reattach the controlling terminal to stdin before handing off to the agent.

    Completing the browser SSO login can leave stdin detached from the terminal,
    which makes a TUI agent like Claude Code start in non-interactive mode and
    exit immediately. Reopening /dev/tty onto fd 0 gives the agent a live
    terminal; when stdin is still a tty (no login happened) this is a no-op.
    """
    if sys.stdin.isatty():
        return
    try:
        fd = os.open("/dev/tty", os.O_RDONLY)
    except OSError:
        return
    try:
        os.dup2(fd, 0)
    finally:
        os.close(fd)

