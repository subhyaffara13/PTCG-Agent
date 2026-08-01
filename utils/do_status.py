
def do_status(args: argparse.Namespace) -> None:
    """Print daemon status.

    This verifies that it is responsive to requests.
    """
    status = read_status(args.status_file)
    if args.verbose:
        show_stats(status)
    # Both check_status() and request() may raise BadStatus,
    # which will be handled by main().
    check_status(status)
    response = request(
        args.status_file, "status", fswatcher_dump_file=args.fswatcher_dump_file, timeout=5
    )
    if args.verbose or "error" in response:
        show_stats(response)
    if "error" in response:
        fail(f"Daemon may be busy processing; if this persists, consider {sys.argv[0]} kill")
    print("Daemon is up and running")

