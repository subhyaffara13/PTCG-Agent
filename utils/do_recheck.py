import time

def do_recheck(args: argparse.Namespace) -> None:
    """Ask the daemon to recheck the previous list of files, with optional modifications.

    If at least one of --remove or --update is given, the server will
    update the list of files to check accordingly and assume that any other files
    are unchanged.  If none of these flags are given, the server will call stat()
    on each file last checked to determine its status.

    Files given in --update ought to exist.  Files given in --remove need not exist;
    if they don't they will be ignored.
    The lists may be empty but oughtn't contain duplicates or overlap.

    NOTE: The list of files is lost when the daemon is restarted.
    """
    t0 = time.time()
    if args.remove is not None or args.update is not None:
        response = request(
            args.status_file,
            "recheck",
            export_types=args.export_types,
            remove=args.remove,
            update=args.update,
        )
    else:
        response = request(args.status_file, "recheck", export_types=args.export_types)
    t1 = time.time()
    response["roundtrip_time"] = t1 - t0
    check_output(response, args.verbose, args.junit_xml, args.perf_stats_file)

