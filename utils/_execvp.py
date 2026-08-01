
def _execvp(cmd: str, argv: list[str]) -> None:
    """execvp, except on Windows where it uses Popen

    Python provides execvp on Windows, but its behavior is problematic (Python bug#9148).
    """
    if sys.platform.startswith("win"):
        # PATH is ignored when shell=False,
        # so rely on shutil.which
        cmd_path = which(cmd)
        if cmd_path is None:
            msg = f"{cmd!r} not found"
            raise OSError(msg, errno.ENOENT)
        p = Popen([cmd_path, *argv[1:]])  # noqa: S603
        # Don't raise KeyboardInterrupt in the parent process.
        # Set this after spawning, to avoid subprocess inheriting handler.
        import signal  # noqa: PLC0415

        signal.signal(signal.SIGINT, signal.SIG_IGN)
        p.wait()
        sys.exit(p.returncode)
    else:
        os.execvp(cmd, argv)  # noqa: S606

