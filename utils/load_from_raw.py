
def load_from_raw(
    fnam: str,
    module: str | None,
    raw_data: FileRawData,
    errors: Errors,
    options: Options,
    imports_only: bool = False,
) -> MypyFile:
    """Load AST from parsed binary data and report stored errors.

    If imports_only is true, only deserialize imports and return a mostly
    empty AST.
    """
    from mypy.nativeparse import State, deserialize_imports, read_statements

    state = State(options, is_stub=fnam.endswith(".pyi"))
    if imports_only:
        defs = []
    else:
        data = ReadBuffer(raw_data.defs)
        n = read_int(data)
        defs = read_statements(state, data, n)
    imports = deserialize_imports(raw_data.imports)

    tree = MypyFile(defs, imports)
    tree.path = fnam
    tree.ignored_lines = raw_data.ignored_lines
    tree.is_partial_stub_package = raw_data.is_partial_stub_package
    tree.uses_template_strings = raw_data.uses_template_strings
    tree.is_stub = fnam.endswith(".pyi")
    if module is not None:
        tree._fullname = module

    # Report parse errors, this replicates the logic in parse().
    all_errors = raw_data.raw_errors + state.errors
    errors.set_file(fnam, module, options=options)
    for error in all_errors:
        # Note we never raise in this function, so it should not be called in coordinator.
        report_parse_error(error, errors)
    if imports_only:
        # Preserve raw data when only de-serializing imports, it will be sent to
        # the parallel workers.
        tree.raw_data = raw_data
    return tree

