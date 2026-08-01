
def do_restart(args: argparse.Namespace) -> None:
    """Restart daemon (it may or may not be running; but not hanging).

    We first try to stop it politely if it's running.  This also sets
    mypy flags from the command line (see do_start()).
    """
    restart_server(args)

