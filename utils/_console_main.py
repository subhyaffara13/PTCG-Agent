
def _console_main() -> int:
    """The CLI entry point of pytest (internal).

    This is the real implementation used by entry points and ``__main__.py``.
    """
    # https://docs.python.org/3/library/signal.html#note-on-sigpipe
    try:
        code = _main(prog=_get_prog_name(sys.argv))
        sys.stdout.flush()
        return code
    except BrokenPipeError:
        # Python flushes standard streams on exit; redirect remaining output
        # to devnull to avoid another BrokenPipeError at shutdown
        devnull = os.open(os.devnull, os.O_WRONLY)
        os.dup2(devnull, sys.stdout.fileno())
        return 1  # Python exits with error code 1 on EPIPE

