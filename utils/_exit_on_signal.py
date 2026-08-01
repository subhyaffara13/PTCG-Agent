
def _exitOnSignal(sigName, message):
    """Handles a signal with sys.exit.

    Some of these signals (SIGPIPE, for example) don't exist or are invalid on
    Windows. So, ignore errors that might arise.
    """
    import signal

    try:
        sigNumber = getattr(signal, sigName)
    except AttributeError:
        # the signal constants defined in the signal module are defined by
        # whether the C library supports them or not. So, SIGPIPE might not
        # even be defined.
        return

    def handler(sig, f):
        sys.exit(message)

    try:
        signal.signal(sigNumber, handler)
    except ValueError:
        # It's also possible the signal is defined, but then it's invalid. In
        # this case, signal.signal raises ValueError.
        pass

