
def restart_server(args: argparse.Namespace, allow_sources: bool = False) -> None:
    """Restart daemon (it may or may not be running; but not hanging)."""
    try:
        do_stop(args)
    except BadStatus:
        # Bad or missing status file or dead process; good to start.
        pass
    start_server(args, allow_sources)

