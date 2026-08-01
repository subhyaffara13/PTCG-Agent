
def do_inspect(args: argparse.Namespace) -> None:
    """Ask daemon to print the type of an expression."""
    response = request(
        args.status_file,
        "inspect",
        show=args.show,
        location=args.location,
        verbosity=args.verbose,
        limit=args.limit,
        include_span=args.include_span,
        include_kind=args.include_kind,
        include_object_attrs=args.include_object_attrs,
        union_attrs=args.union_attrs,
        force_reload=args.force_reload,
    )
    check_output(response, verbose=False, junit_xml=None, perf_stats_file=None)

