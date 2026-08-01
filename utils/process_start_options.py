
def process_start_options(flags: list[str], allow_sources: bool) -> Options:
    _, options = mypy.main.process_options(
        ["-i"] + flags, require_targets=False, server_options=True
    )
    if options.report_dirs:
        print("dmypy: Ignoring report generation settings. Start/restart cannot generate reports.")
    if options.junit_xml:
        print(
            "dmypy: Ignoring report generation settings. "
            "Start/restart does not support --junit-xml. Pass it to check/recheck instead"
        )
        options.junit_xml = None
    if not options.incremental:
        sys.exit("dmypy: start/restart should not disable incremental mode")
    if options.follow_imports not in ("skip", "error", "normal"):
        sys.exit("dmypy: follow-imports=silent not supported")
    if not options.local_partial_types:
        sys.exit("dmypy: disabling local-partial-types not supported")
    return options

