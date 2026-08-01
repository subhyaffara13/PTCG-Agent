
def do_hang(args: argparse.Namespace) -> None:
    """Hang for 100 seconds, as a debug hack."""
    print(request(args.status_file, "hang", timeout=1))

