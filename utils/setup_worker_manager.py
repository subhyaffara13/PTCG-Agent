
def setup_worker_manager(sources: list[BuildSource], ctx: ServerContext) -> BuildManager | None:
    data_dir = os.path.dirname(os.path.dirname(__file__))
    # This is used for testing only now.
    alt_lib_path = os.environ.get("MYPY_ALT_LIB_PATH")
    search_paths = compute_search_paths(sources, ctx.options, data_dir, alt_lib_path)

    source_set = BuildSourceSet(sources)
    try:
        plugin, snapshot = load_plugins(ctx.options, ctx.errors, sys.stdout, [])
    except CompileError:
        # CompileError while importing plugins will be reported by the coordinator.
        return None

    # Process the rest of the options when plugins are loaded.
    options = ctx.options
    options.disable_error_code = ctx.disable_error_code
    options.enable_error_code = ctx.enable_error_code
    options.process_error_codes(error_callback=lambda msg: None)

    def flush_errors(filename: str | None, new_messages: list[str], is_serious: bool) -> None:
        # We never flush errors in the worker, we send them back to coordinator.
        pass

    try:
        return BuildManager(
            data_dir,
            search_paths,
            ignore_prefix=os.getcwd(),
            source_set=source_set,
            reports=None,
            options=options,
            version_id=__version__,
            plugin=plugin,
            plugins_snapshot=snapshot,
            errors=ctx.errors,
            error_formatter=None if options.output is None else OUTPUT_CHOICES.get(options.output),
            flush_errors=flush_errors,
            fscache=ctx.fscache,
            stdout=sys.stdout,
            stderr=sys.stderr,
            parallel_worker=True,
        )
    except CompileError:
        return None

