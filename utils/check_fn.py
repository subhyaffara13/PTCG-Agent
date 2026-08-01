
def check_fn(fn, loc) -> None:
    # Make sure the function definition is not a class instantiation
    try:
        source = dedent("".join(get_source_lines_and_file(fn)[0]))
    except (OSError, TypeError):
        return
    if source is None:
        return

    py_ast = ast.parse(source)
    if len(py_ast.body) == 1 and isinstance(py_ast.body[0], ast.ClassDef):
        raise torch.jit.frontend.FrontendError(
            loc,
            f"Cannot instantiate class '{py_ast.body[0].name}' in a script function",
        )
    if len(py_ast.body) != 1 or not isinstance(py_ast.body[0], ast.FunctionDef):
        raise torch.jit.frontend.FrontendError(
            loc, "Expected a single top-level function"
        )

