import os
import sys

def process_options(arglist=None, parse_argv=False, config_file=None,
                    parser=None, verbose=None):
    """Process options passed either via arglist or command line args.

    Passing in the ``config_file`` parameter allows other tools, such as
    flake8 to specify their own options to be processed in pycodestyle.
    """
    if not parser:
        parser = get_parser()
    if not parser.has_option('--config'):
        group = parser.add_option_group("Configuration", description=(
            "The project options are read from the [%s] section of the "
            "tox.ini file or the setup.cfg file located in any parent folder "
            "of the path(s) being processed.  Allowed options are: %s." %
            (parser.prog, ', '.join(parser.config_options))))
        group.add_option('--config', metavar='path', default=config_file,
                         help="user config file location")
    # Don't read the command line if the module is used as a library.
    if not arglist and not parse_argv:
        arglist = []
    # If parse_argv is True and arglist is None, arguments are
    # parsed from the command line (sys.argv)
    (options, args) = parser.parse_args(arglist)
    options.reporter = None

    # If explicitly specified verbosity, override any `-v` CLI flag
    if verbose is not None:
        options.verbose = verbose

    if parse_argv and not args:
        if options.diff or any(os.path.exists(name)
                               for name in PROJECT_CONFIG):
            args = ['.']
        else:
            parser.error('input not specified')
    options = read_config(options, args, arglist, parser)
    options.reporter = parse_argv and options.quiet == 1 and FileReport

    options.filename = _parse_multi_options(options.filename)
    options.exclude = normalize_paths(options.exclude)
    options.select = _parse_multi_options(options.select)
    options.ignore = _parse_multi_options(options.ignore)

    if options.diff:
        options.reporter = DiffReport
        stdin = stdin_get_value()
        options.selected_lines = parse_udiff(stdin, options.filename, args[0])
        args = sorted(options.selected_lines)

    return options, args


def process_options(
    args: list[str],
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
    require_targets: bool = True,
    server_options: bool = False,
    fscache: FileSystemCache | None = None,
    program: str = "mypy",
    header: str = HEADER,
    mypyc: bool = False,
) -> tuple[list[BuildSource], Options]:
    """Parse command line arguments.

    If a FileSystemCache is passed in, and package_root options are given,
    call fscache.set_package_root() to set the cache's package root.

    Returns a tuple of: a list of source files, an Options collected from flags.
    """
    stdout = stdout if stdout is not None else sys.stdout
    stderr = stderr if stderr is not None else sys.stderr

    parser, _, strict_flag_assignments = define_options(
        program, header, stdout, stderr, server_options
    )

    # Parse arguments once into a dummy namespace so we can get the
    # filename for the config file and know if the user requested all strict options.
    dummy = argparse.Namespace()
    parser.parse_args(args, dummy)
    config_file = dummy.config_file
    # Don't explicitly test if "config_file is not None" for this check.
    # This lets `--config-file=` (an empty string) be used to disable all config files.
    if config_file and not os.path.exists(config_file):
        parser.error(f"Cannot find config file '{config_file}'")

    options = Options()
    strict_option_set = False
    if mypyc:
        # Mypyc has strict_bytes enabled by default
        options.strict_bytes = True

    def set_strict_flags() -> None:
        nonlocal strict_option_set
        strict_option_set = True
        for dest, value in strict_flag_assignments:
            setattr(options, dest, value)

    # Parse config file first, so command line can override.
    parse_config_file(options, set_strict_flags, config_file, stdout, stderr)

    # Set strict flags before parsing (if strict mode enabled), so other command
    # line options can override.
    if getattr(dummy, "special-opts:strict"):
        set_strict_flags()

    # Override cache_dir if provided in the environment
    environ_cache_dir = os.getenv("MYPY_CACHE_DIR", "")
    if environ_cache_dir.strip():
        options.cache_dir = environ_cache_dir
    options.cache_dir = os.path.expanduser(options.cache_dir)

    # Override num_workers if provided in the environment
    environ_num_workers = os.getenv("MYPY_NUM_WORKERS", "")
    if environ_num_workers.strip():
        try:
            options.num_workers = int(environ_num_workers)
        except ValueError:
            parser.error(f"MYPY_NUM_WORKERS must be an integer, got {environ_num_workers!r}")

    # Parse command line for real, using a split namespace.
    special_opts = argparse.Namespace()
    parser.parse_args(args, SplitNamespace(options, special_opts, "special-opts:"))

    # The python_version is either the default, which can be overridden via a config file,
    # or stored in special_opts and is passed via the command line.
    options.python_version = special_opts.python_version or options.python_version
    if options.python_version < (3,):
        parser.error(
            "Mypy no longer supports checking Python 2 code. "
            "Consider pinning to mypy<0.980 if you need to check Python 2 code."
        )
    try:
        infer_python_executable(options, special_opts)
    except PythonExecutableInferenceError as e:
        parser.error(str(e))

    if special_opts.no_executable or options.no_site_packages:
        options.python_executable = None

    # Paths listed in the config file will be ignored if any paths, modules or packages
    # are passed on the command line.
    if not (special_opts.files or special_opts.packages or special_opts.modules):
        if options.files:
            special_opts.files = options.files
        if options.packages:
            special_opts.packages = options.packages
        if options.modules:
            special_opts.modules = options.modules

    # Check for invalid argument combinations.
    if require_targets:
        code_methods = sum(
            bool(c)
            for c in [
                special_opts.modules + special_opts.packages,
                special_opts.command,
                special_opts.files,
            ]
        )
        if code_methods == 0 and not options.install_types:
            parser.error("Missing target module, package, files, or command.")
        elif code_methods > 1:
            parser.error("May only specify one of: module/package, files, or command.")
    if options.explicit_package_bases and not options.namespace_packages:
        parser.error(
            "Can only use --explicit-package-bases with --namespace-packages, since otherwise "
            "examining __init__.py's is sufficient to determine module names for files"
        )

    # Check for overlapping `--always-true` and `--always-false` flags.
    overlap = set(options.always_true) & set(options.always_false)
    if overlap:
        parser.error(
            "You can't make a variable always true and always false (%s)"
            % ", ".join(sorted(overlap))
        )

    validate_package_allow_list(options.untyped_calls_exclude)
    validate_package_allow_list(options.deprecated_calls_exclude)

    options.process_incomplete_features(error_callback=parser.error, warning_callback=print)

    # Compute absolute path for custom typeshed (if present).
    if options.custom_typeshed_dir is not None:
        options.abs_custom_typeshed_dir = os.path.abspath(options.custom_typeshed_dir)

    # Set build flags.
    if special_opts.find_occurrences:
        _find_occurrences = tuple(special_opts.find_occurrences.split("."))
        if len(_find_occurrences) < 2:
            parser.error("Can only find occurrences of class members.")
        if len(_find_occurrences) != 2:
            parser.error("Can only find occurrences of non-nested class members.")
        state.find_occurrences = _find_occurrences

    # Set reports.
    for flag, val in vars(special_opts).items():
        if flag.endswith("_report") and val is not None:
            report_type = flag[:-7].replace("_", "-")
            report_dir = val
            options.report_dirs[report_type] = report_dir

    # Process --package-root.
    if options.package_root:
        process_package_roots(fscache, parser, options)

    # Process --cache-map.
    if special_opts.cache_map:
        if options.sqlite_cache:
            parser.error("--cache-map is incompatible with --sqlite-cache")

        process_cache_map(parser, special_opts, options)

    # Process --strict-bytes
    options.process_strict_bytes()

    # An explicitly specified cache_fine_grained implies local_partial_types
    # (because otherwise the cache is not compatible with dmypy)
    if options.cache_fine_grained:
        options.local_partial_types = True

    #  Implicitly show column numbers if error location end is shown
    if options.show_error_end:
        options.show_column_numbers = True

    # Let logical_deps imply cache_fine_grained (otherwise the former is useless).
    if options.logical_deps:
        options.cache_fine_grained = True

    if options.strict_concatenate and not strict_option_set:
        print("Warning: --strict-concatenate is deprecated; use --extra-checks instead")

    # Set target.
    if special_opts.modules + special_opts.packages:
        options.build_type = BuildType.MODULE
        sys_path, _ = get_search_dirs(options.python_executable)
        search_paths = SearchPaths(
            (os.getcwd(),), tuple(mypy_path() + options.mypy_path), tuple(sys_path), ()
        )
        targets = []
        # TODO: use the same cache that the BuildManager will
        cache = FindModuleCache(search_paths, fscache, options)
        for p in special_opts.packages:
            if os.sep in p or os.altsep and os.altsep in p:
                fail(f"Package name '{p}' cannot have a slash in it.", stderr, options)
            p_targets = cache.find_modules_recursive(p)
            if not p_targets:
                reason = cache.find_module(p)
                if reason is ModuleNotFoundReason.FOUND_WITHOUT_TYPE_HINTS:
                    fail(
                        f"Package '{p}' cannot be type checked due to missing py.typed marker.\n"
                        "See https://mypy.readthedocs.io/en/stable/installed_packages.html for more details",
                        stderr,
                        options,
                    )
                else:
                    fail(f"Can't find package '{p}'", stderr, options)
            targets.extend(p_targets)
        for m in special_opts.modules:
            targets.append(BuildSource(None, m, None))
    elif special_opts.command:
        options.build_type = BuildType.PROGRAM_TEXT
        targets = [BuildSource(None, None, "\n".join(special_opts.command))]
    else:
        try:
            targets = create_source_list(special_opts.files, options, fscache)
        # Variable named e2 instead of e to work around mypyc bug #620
        # which causes issues when using the same variable to catch
        # exceptions of different types.
        except InvalidSourceList as e2:
            fail(str(e2), stderr, options)
    return targets, options

