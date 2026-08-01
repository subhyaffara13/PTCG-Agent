
def parse_def(fn):
    sourcelines, file_lineno, filename = get_source_lines_and_file(
        fn, ErrorReport.call_stack()
    )
    sourcelines = normalize_source_lines(sourcelines)
    source = "".join(sourcelines)
    dedent_src = dedent(source)
    py_ast = ast.parse(dedent_src)
    if len(py_ast.body) != 1 or not isinstance(py_ast.body[0], ast.FunctionDef):
        raise RuntimeError(
            f"Expected a single top-level function: {filename}:{file_lineno}"
        )
    leading_whitespace_len = len(source.split("\n", 1)[0]) - len(
        dedent_src.split("\n", 1)[0]
    )
    ctx = make_source_context(
        source, filename, file_lineno, leading_whitespace_len, True, fn.__name__
    )
    return ParsedDef(py_ast, ctx, source, filename, file_lineno)

