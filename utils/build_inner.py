
def build_inner(
    sources: list[BuildSource],
    options: Options,
    alt_lib_path: str | None,
    flush_errors: Callable[[str | None, list[str], bool], None],
    fscache: FileSystemCache | None,
    stdout: TextIO,
    stderr: TextIO,
    extra_plugins: Sequence[Plugin],
    workers: list[WorkerClient],
    connect_threads: list[Thread],
    metastore: MetadataStore,
) -> BuildResult:
    if platform.python_implementation() == "CPython":
        # Run gc less frequently, as otherwise we can spend a large fraction of
        # cpu in gc. This seems the most reasonable place to tune garbage collection.
        gc.set_threshold(200 * 1000, 30, 30)

    data_dir = default_data_dir()
    fscache = fscache or FileSystemCache()

    search_paths = compute_search_paths(sources, options, data_dir, alt_lib_path)

    reports = None
    if options.report_dirs:
        # Import lazily to avoid slowing down startup.
        from mypy.report import Reports

        reports = Reports(data_dir, options.report_dirs)

    source_set = BuildSourceSet(sources)
    cached_read = fscache.read
    error_formatter = None if options.output is None else OUTPUT_CHOICES.get(options.output)
    errors = Errors(
        options,
        read_source=lambda path: read_py_file(path, cached_read),
        error_formatter=error_formatter,
    )
    # Record import errors so that they can be replayed by the workers.
    if workers:
        errors.global_watcher = True
    plugin, snapshot = load_plugins(options, errors, stdout, extra_plugins)

    # Validate error codes after plugins are loaded.
    options.process_error_codes(error_callback=build_error)

    # Construct a build manager object to hold state during the build.
    #
    # Ignore current directory prefix in error messages.
    manager = BuildManager(
        data_dir,
        search_paths,
        ignore_prefix=os.getcwd(),
        source_set=source_set,
        reports=reports,
        options=options,
        version_id=__version__,
        plugin=plugin,
        plugins_snapshot=snapshot,
        errors=errors,
        error_formatter=error_formatter,
        flush_errors=flush_errors,
        fscache=fscache,
        stdout=stdout,
        stderr=stderr,
        metastore=metastore,
    )
    manager.workers = workers
    if manager.verbosity() >= 2:
        manager.trace(repr(options))

    reset_global_state()
    try:
        graph = dispatch(sources, manager, stdout, connect_threads)
        if not options.fine_grained_incremental:
            type_state.reset_all_subtype_caches()
        if options.timing_stats is not None:
            dump_timing_stats(options.timing_stats, graph)
        if options.line_checking_stats is not None:
            dump_line_checking_stats(options.line_checking_stats, graph)
        warn_unused_configs(options, flush_errors)
        return BuildResult(manager, graph)
    finally:
        manager.commit()
        manager.log(
            "Build finished in %.3f seconds with %d modules, and %d errors"
            % (
                time.time() - manager.start_time,
                len(manager.modules),
                manager.errors.num_messages(),
            )
        )
        manager.dump_stats()
        if reports is not None:
            # Finish the HTML or XML reports even if CompileError was raised.
            reports.finish()
        if os.path.isdir(options.cache_dir):
            add_catch_all_gitignore(options.cache_dir)
            exclude_from_backups(options.cache_dir)
        if os.path.isdir(options.cache_dir):
            record_missing_stub_packages(options.cache_dir, manager.missing_stub_packages)

