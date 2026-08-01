
def do_daemon(args: argparse.Namespace) -> None:
    """Serve requests in the foreground."""
    # Lazy import so this import doesn't slow down other commands.
    from mypy.dmypy_server import Server, process_start_options

    if args.log_file:
        sys.stdout = sys.stderr = open(args.log_file, "a", buffering=1)
        fd = sys.stdout.fileno()
        os.dup2(fd, 2)
        os.dup2(fd, 1)

    if args.options_data:
        from mypy.options import Options

        options_dict = pickle.loads(b64decode(args.options_data))
        options_obj = Options()
        options = options_obj.apply_changes(options_dict)
    else:
        options = process_start_options(args.flags, allow_sources=False)

    Server(options, args.status_file, timeout=args.timeout).serve()

