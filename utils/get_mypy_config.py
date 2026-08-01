
def get_mypy_config(
    mypy_options: list[str],
    only_compile_paths: Iterable[str] | None,
    compiler_options: CompilerOptions,
    fscache: FileSystemCache | None,
) -> tuple[list[BuildSource], list[BuildSource], Options]:
    """Construct mypy BuildSources and Options from file and options lists"""
    all_sources, options = process_options(mypy_options, fscache=fscache, mypyc=True)
    if only_compile_paths is not None:
        paths_set = set(only_compile_paths)
        mypyc_sources = [s for s in all_sources if s.path in paths_set]
    else:
        mypyc_sources = all_sources

    if compiler_options.separate:
        mypyc_sources = [src for src in mypyc_sources if src.path]

    if not mypyc_sources:
        return mypyc_sources, all_sources, options

    # Override whatever python_version is inferred from the .ini file,
    # and set the python_version to be the currently used version.
    options.python_version = sys.version_info[:2]

    if options.python_version[0] == 2:
        fail("Python 2 not supported")
    if not options.strict_optional:
        fail("Disabling strict optional checking not supported")
    options.show_traceback = True
    # Needed to get types for all AST nodes
    options.export_types = True
    # We use mypy incremental mode when doing separate/incremental mypyc compilation
    options.incremental = compiler_options.separate
    options.preserve_asts = True

    for source in mypyc_sources:
        options.per_module_options.setdefault(source.module, {})["mypyc"] = True

    return mypyc_sources, all_sources, options

