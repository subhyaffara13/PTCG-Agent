
def test_stubs(args: _Arguments, use_builtins_fixtures: bool = False) -> int:
    """This is stubtest! It's time to test the stubs!"""
    # Load the allowlist. This is a series of strings corresponding to Error.object_desc
    # Values in the dict will store whether we used the allowlist entry or not.
    allowlist = {
        entry: False
        for allowlist_file in args.allowlist
        for entry in get_allowlist_entries(allowlist_file)
    }
    allowlist_regexes = {entry: re.compile(entry) for entry in allowlist}

    # If we need to generate an allowlist, we store Error.object_desc for each error here.
    generated_allowlist = set()

    modules = args.modules
    if args.check_typeshed:
        if args.modules:
            print(
                _style("error:", color="red", bold=True),
                "cannot pass both --check-typeshed and a list of modules",
            )
            return 1
        typeshed_modules = get_typeshed_stdlib_modules(args.custom_typeshed_dir)
        runtime_modules = get_importable_stdlib_modules()
        modules = sorted((typeshed_modules | runtime_modules) - ANNOYING_STDLIB_MODULES)

    if not modules:
        print(_style("error:", color="red", bold=True), "no modules to check")
        return 1

    options = Options()
    options.incremental = False
    options.custom_typeshed_dir = args.custom_typeshed_dir
    if options.custom_typeshed_dir:
        options.abs_custom_typeshed_dir = os.path.abspath(options.custom_typeshed_dir)
    options.config_file = args.mypy_config_file
    options.use_builtins_fixtures = use_builtins_fixtures
    options.show_traceback = args.show_traceback
    options.pdb = args.pdb
    options.pos_only_special_methods = False

    if options.config_file:

        def set_strict_flags() -> None:  # not needed yet
            return

        parse_config_file(options, set_strict_flags, options.config_file, sys.stdout, sys.stderr)

    def error_callback(msg: str) -> typing.NoReturn:
        print(_style("error:", color="red", bold=True), msg)
        sys.exit(1)

    def warning_callback(msg: str) -> None:
        print(_style("warning:", color="yellow", bold=True), msg)

    options.process_error_codes(error_callback=error_callback)
    options.process_incomplete_features(
        error_callback=error_callback, warning_callback=warning_callback
    )
    options.process_strict_bytes()

    try:
        modules = build_stubs(modules, options, find_submodules=not args.check_typeshed)
    except StubtestFailure as stubtest_failure:
        print(
            _style("error:", color="red", bold=True),
            f"not checking stubs due to {stubtest_failure}",
        )
        return 1

    exit_code = 0
    error_count = 0
    for module in modules:
        for error in test_module(module):
            # Filter errors
            if args.ignore_missing_stub and error.is_missing_stub():
                continue
            if args.ignore_positional_only and error.is_positional_only_related():
                continue
            if args.ignore_disjoint_bases and error.is_disjoint_base_related():
                continue
            if not args.strict_type_check_only and error.is_private_type_check_only_related():
                continue
            if error.object_desc in allowlist:
                allowlist[error.object_desc] = True
                continue
            is_allowlisted = False
            for w in allowlist:
                if allowlist_regexes[w].fullmatch(error.object_desc):
                    allowlist[w] = True
                    is_allowlisted = True
                    break
            if is_allowlisted:
                continue

            # We have errors, so change exit code, and output whatever necessary
            exit_code = 1
            if args.generate_allowlist:
                generated_allowlist.add(error.object_desc)
                continue
            safe_print(error.get_description(concise=args.concise))
            error_count += 1

    # Print unused allowlist entries
    if not args.ignore_unused_allowlist:
        for w in allowlist:
            # Don't consider an entry unused if it regex-matches the empty string
            # This lets us allowlist errors that don't manifest at all on some systems
            if not allowlist[w] and not allowlist_regexes[w].fullmatch(""):
                exit_code = 1
                error_count += 1
                print(f"note: unused allowlist entry {w}")

    # Print the generated allowlist
    if args.generate_allowlist:
        for e in sorted(generated_allowlist):
            print(e)
        exit_code = 0
    elif not args.concise:
        if error_count:
            print(
                _style(
                    f"Found {error_count} error{plural_s(error_count)}"
                    f" (checked {len(modules)} module{plural_s(modules)})",
                    color="red",
                    bold=True,
                )
            )
        else:
            print(
                _style(
                    f"Success: no issues found in {len(modules)} module{plural_s(modules)}",
                    color="green",
                    bold=True,
                )
            )

    return exit_code

