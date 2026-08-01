
def parse_to_binary_ast(
    filename: str,
    options: Options,
    source: str | bytes | None = None,
    skip_function_bodies: bool = False,
) -> tuple[bytes, list[ParseError], TypeIgnores, bytes, bool, bool, str, list[tuple[int, str]]]:
    # This is a horrible hack to work around a mypyc bug where imported
    # module may be not ready in a thread sometimes.
    t0 = time.time()
    while ast_serialize is None:
        time.sleep(0.0001)  # type: ignore[unreachable]
        if time.time() - t0 > 10.0:
            raise ImportError("Cannot import ast_serialize")
    ast_bytes, errors, ignores, import_bytes, ast_data = ast_serialize.parse(
        filename,
        source,
        skip_function_bodies=skip_function_bodies,
        python_version=options.python_version,
        platform=options.platform,
        always_true=options.always_true,
        always_false=options.always_false,
        cache_version=3,
    )
    return (
        ast_bytes,
        errors,
        ignores,
        import_bytes,
        ast_data["is_partial_package"],
        ast_data["uses_template_strings"],
        ast_data["source_hash"],
        ast_data["mypy_comments"],
    )

