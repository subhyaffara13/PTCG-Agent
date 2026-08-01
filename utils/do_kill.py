
def do_kill(args: argparse.Namespace) -> None:
    """Kill daemon process with SIGKILL."""
    pid, _ = get_status(args.status_file)
    try:
        kill(pid)
    except OSError as err:
        fail(str(err))
    else:
        print("Daemon killed")

