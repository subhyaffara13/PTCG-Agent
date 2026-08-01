
def run_build(
    sources: list[BuildSource],
    options: Options,
    fscache: FileSystemCache,
    t0: float,
    stdout: TextIO,
    stderr: TextIO,
) -> tuple[BuildResultThunk | None, list[str], bool]:
    formatter = util.FancyFormatter(
        stdout, stderr, options.hide_error_codes, hide_success=bool(options.output)
    )

    messages = []
    messages_by_file = defaultdict(list)

    def flush_errors(filename: str | None, new_messages: list[str], serious: bool) -> None:
        if options.pretty:
            new_messages = formatter.fit_in_terminal(new_messages)
        messages.extend(new_messages)
        if new_messages:
            messages_by_file[filename].extend(new_messages)
        if options.non_interactive:
            # Collect messages and possibly show them later.
            return
        f = stderr if serious else stdout
        show_messages(new_messages, f, formatter, options)

    serious = False
    blockers = False
    res = None
    try:
        # Keep a dummy reference (res) for memory profiling afterwards, as otherwise
        # the result could be freed.
        res = build.build(sources, options, None, flush_errors, fscache, stdout, stderr)
    except CompileError as e:
        blockers = True
        if not e.use_stdout:
            serious = True

    if res:
        res.manager.metastore.close()

    maybe_write_junit_xml(time.time() - t0, serious, messages, messages_by_file, options)
    return BuildResultThunk(res), messages, blockers

