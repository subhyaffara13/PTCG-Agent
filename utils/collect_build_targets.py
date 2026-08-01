
def collect_build_targets(
    options: Options, mypy_opts: MypyOptions
) -> tuple[list[StubSource], list[StubSource], list[StubSource]]:
    """Collect files for which we need to generate stubs.

    Return list of py modules, pyc modules, and C modules.
    """
    if options.packages or options.modules:
        if options.no_import:
            py_modules = find_module_paths_using_search(
                options.modules, options.packages, options.search_path, options.pyversion
            )
            c_modules: list[StubSource] = []
        else:
            # Using imports is the default, since we can also find C modules.
            py_modules, c_modules = find_module_paths_using_imports(
                options.modules, options.packages, options.verbose, options.quiet
            )
    else:
        # Use mypy native source collection for files and directories.
        try:
            source_list = create_source_list(options.files, mypy_opts)
        except InvalidSourceList as e:
            raise SystemExit(str(e)) from e
        py_modules = [StubSource(m.module, m.path) for m in source_list]
        c_modules = []

    py_modules = remove_blacklisted_modules(py_modules)
    pyc_mod, py_mod = split_pyc_from_py(py_modules)
    return py_mod, pyc_mod, c_modules

