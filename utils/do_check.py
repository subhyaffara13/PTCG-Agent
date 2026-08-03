import time

def do_check(args: argparse.Namespace) -> None:
    """Ask the daemon to check a list of files."""
    t0 = time.time()
    response = request(args.status_file, "check", files=args.files, export_types=args.export_types)
    t1 = time.time()
    response["roundtrip_time"] = t1 - t0
    check_output(response, args.verbose, args.junit_xml, args.perf_stats_file)

