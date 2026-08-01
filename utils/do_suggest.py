
def do_suggest(args: argparse.Namespace) -> None:
    """Ask the daemon for a suggested signature.

    This just prints whatever the daemon reports as output.
    For now it may be closer to a list of call sites.
    """
    response = request(
        args.status_file,
        "suggest",
        function=args.function,
        json=args.json,
        callsites=args.callsites,
        no_errors=args.no_errors,
        no_any=args.no_any,
        flex_any=args.flex_any,
        use_fixme=args.use_fixme,
        max_guesses=args.max_guesses,
    )
    check_output(response, verbose=False, junit_xml=None, perf_stats_file=None)

