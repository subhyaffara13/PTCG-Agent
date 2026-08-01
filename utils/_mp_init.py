
def _mp_init(argv: Sequence[str]) -> None:
    global _mp_plugins, _mp_options

    # Ensure correct signaling of ^C using multiprocessing.Pool.
    signal.signal(signal.SIGINT, signal.SIG_IGN)

    try:
        # for `fork` this'll already be set
        _mp_plugins, _mp_options  # noqa: B018
    except NameError:
        plugins, options = parse_args(argv)
        _mp_plugins, _mp_options = plugins.checkers, options

