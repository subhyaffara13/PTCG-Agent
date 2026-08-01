
def generate_asts_for_modules(
    py_modules: list[StubSource], parse_only: bool, mypy_options: MypyOptions, verbose: bool
) -> None:
    """Use mypy to parse (and optionally analyze) source files."""
    if not py_modules:
        return  # Nothing to do here, but there may be C modules
    if verbose:
        print(f"Processing {len(py_modules)} files...")
    if parse_only:
        for mod in py_modules:
            parse_source_file(mod, mypy_options)
        return
    # Perform full semantic analysis of the source set.
    try:
        res = build([module.source for module in py_modules], mypy_options)
    except CompileError as e:
        raise SystemExit(f"Critical error during semantic analysis: {e}") from e

    for mod in py_modules:
        mod.ast = res.graph[mod.module].tree
        # Use statically inferred __all__ if there is no runtime one.
        if mod.runtime_all is None:
            mod_names = res.manager.semantic_analyzer.modules[mod.module].names
            if "__all__" in mod_names:
                mod.runtime_all = [name for name, sym in mod_names.items() if sym.module_public]

