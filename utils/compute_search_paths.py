
def compute_search_paths(
    sources: list[BuildSource], options: Options, data_dir: str, alt_lib_path: str | None = None
) -> SearchPaths:
    """Compute the search paths as specified in PEP 561.

    There are the following 4 members created:
    - User code (from `sources`)
    - MYPYPATH (set either via config or environment variable)
    - installed package directories (which will later be split into stub-only and inline)
    - typeshed
    """
    # Determine the default module search path.
    lib_path = collections.deque(
        default_lib_path(
            data_dir, options.python_version, custom_typeshed_dir=options.custom_typeshed_dir
        )
    )

    if options.use_builtins_fixtures:
        # Use stub builtins (to speed up test cases and to make them easier to
        # debug).  This is a test-only feature, so assume our files are laid out
        # as in the source tree.
        # We also need to allow overriding where to look for it. Argh.
        root_dir = os.getenv("MYPY_TEST_PREFIX", None)
        if not root_dir:
            root_dir = os.path.dirname(os.path.dirname(__file__))
        root_dir = os.path.abspath(root_dir)
        lib_path.appendleft(os.path.join(root_dir, "test-data", "unit", "lib-stub"))
    # alt_lib_path is used by some tests to bypass the normal lib_path mechanics.
    # If we don't have one, grab directories of source files.
    python_path: list[str] = []
    if not alt_lib_path:
        for source in sources:
            # Include directory of the program file in the module search path.
            if source.base_dir:
                dir = source.base_dir
                if dir not in python_path:
                    python_path.append(dir)

        # Do this even if running as a file, for sanity (mainly because with
        # multiple builds, there could be a mix of files/modules, so its easier
        # to just define the semantics that we always add the current director
        # to the lib_path
        # TODO: Don't do this in some cases; for motivation see see
        # https://github.com/python/mypy/issues/4195#issuecomment-341915031
        if options.bazel:
            dir = "."
        else:
            dir = os.getcwd()
        if dir not in lib_path:
            python_path.insert(0, dir)

    # Start with a MYPYPATH environment variable at the front of the mypy_path, if defined.
    mypypath = mypy_path()

    # Add a config-defined mypy path.
    mypypath.extend(options.mypy_path)

    # If provided, insert the caller-supplied extra module path to the
    # beginning (highest priority) of the search path.
    if alt_lib_path:
        mypypath.insert(0, alt_lib_path)

    sys_path, site_packages = get_search_dirs(options.python_executable)
    # We only use site packages for this check
    for site in site_packages:
        assert site not in lib_path
        if (
            site in mypypath
            or any(p.startswith(site + os.path.sep) for p in mypypath)
            or (os.path.altsep and any(p.startswith(site + os.path.altsep) for p in mypypath))
        ):
            print(f"{site} is in the MYPYPATH. Please remove it.", file=sys.stderr)
            print(
                "See https://mypy.readthedocs.io/en/stable/running_mypy.html"
                "#how-mypy-handles-imports for more info",
                file=sys.stderr,
            )
            sys.exit(1)

    return SearchPaths(
        python_path=tuple(reversed(python_path)),
        mypy_path=tuple(mypypath),
        package_path=tuple(sys_path + site_packages),
        typeshed_path=tuple(lib_path),
    )

