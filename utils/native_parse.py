import os

def native_parse(
    filename: str,
    options: Options,
    source: str | bytes | None = None,
    skip_function_bodies: bool = False,
) -> tuple[MypyFile, list[ParseError], TypeIgnores]:
    """Parse a Python file using the native Rust-based parser.

    Return (MypyFile, errors, type_ignores).

    The returned tree is empty with actual serialized data stored in `raw_data`
    attribute. Use read_statements() and/or deserialize_imports() to de-serialize.

    The caller should set these additional attributes on the returned MypyFile:
      - ignored_lines: dict of type ignore comments (from the TypeIgnores return value)
      - is_stub: whether the file is a .pyi stub
    """
    # If the path is a directory, return empty AST (matching fastparse behavior)
    # This can happen for packages that only contain .pyc files without source
    if os.path.isdir(filename):
        node = MypyFile([], [])
        node.path = filename
        return node, [], []

    (
        b,
        errors,
        ignores,
        import_bytes,
        is_partial_package,
        uses_template_strings,
        source_hash,
        mypy_comments,
    ) = parse_to_binary_ast(filename, options, source, skip_function_bodies)
    node = MypyFile([], [])
    node.path = filename
    node.raw_data = FileRawData(
        b,
        import_bytes,
        errors,
        dict(ignores),
        is_partial_package,
        uses_template_strings,
        source_hash,
        mypy_comments,
    )
    return node, errors, ignores

