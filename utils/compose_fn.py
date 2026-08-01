
def compose_fn(cls, name: str, body_lines: list[str], signature: str) -> ParsedDef:
    body = "\n".join(f"  {b}" for b in body_lines)
    decl = f"def {name}{signature}:\n{body}"

    # Parse the function declaration
    try:
        py_ast = ast.parse(decl)
    except SyntaxError as e:
        # This should only happen if there's some unforeseeable change
        # in the dataclasses module that makes our synthesized code fail
        raise RuntimeError(
            f"TorchScript failed to synthesize dataclass method '{name}' for class '{cls.__name__}'. "
            "Please file a bug report at <https://github.com/pytorch/pytorch/issues>"
        ) from e
    fake_filename = _get_fake_filename(cls, name)
    # Parse the function
    return ParsedDef(
        py_ast,
        ctx=SourceContext(
            source=decl, filename=fake_filename, file_lineno=0, leading_whitespace_len=0
        ),
        source=decl,
        filename=fake_filename,
        file_lineno=0,
    )

