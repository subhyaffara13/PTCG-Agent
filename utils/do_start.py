
def do_start(args: argparse.Namespace) -> None:
    """Start daemon (it must not already be running).

    This is where mypy flags are set from the command line.

    Setting flags is a bit awkward; you have to use e.g.:

      dmypy start -- --strict

    since we don't want to duplicate mypy's huge list of flags.
    """
    try:
        get_status(args.status_file)
    except BadStatus:
        # Bad or missing status file or dead process; good to start.
        pass
    else:
        fail("Daemon is still alive")
    start_server(args)

