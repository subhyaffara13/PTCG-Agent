import time

def do_run(args: argparse.Namespace) -> None:
    """Do a check, starting (or restarting) the daemon as necessary

    Restarts the daemon if the running daemon reports that it is
    required (due to a configuration change, for example).

    Setting flags is a bit awkward; you have to use e.g.:

      dmypy run -- --strict a.py b.py ...

    since we don't want to duplicate mypy's huge list of flags.
    (The -- is only necessary if flags are specified.)
    """
    if not is_running(args.status_file):
        # Bad or missing status file or dead process; good to start.
        start_server(args, allow_sources=True)
    t0 = time.time()
    response = request(
        args.status_file,
        "run",
        version=__version__,
        args=args.flags,
        export_types=args.export_types,
    )
    # If the daemon signals that a restart is necessary, do it
    if "restart" in response:
        print(f"Restarting: {response['restart']}")
        restart_server(args, allow_sources=True)
        response = request(
            args.status_file,
            "run",
            version=__version__,
            args=args.flags,
            export_types=args.export_types,
        )

    t1 = time.time()
    response["roundtrip_time"] = t1 - t0
    check_output(response, args.verbose, args.junit_xml, args.perf_stats_file)

