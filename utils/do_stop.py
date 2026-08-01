
def do_stop(args: argparse.Namespace) -> None:
    """Stop daemon via a 'stop' request."""
    # May raise BadStatus, which will be handled by main().
    response = request(args.status_file, "stop", timeout=5)
    if "error" in response:
        show_stats(response)
        fail(f"Daemon may be busy processing; if this persists, consider {sys.argv[0]} kill")
    else:
        print("Daemon stopped")

