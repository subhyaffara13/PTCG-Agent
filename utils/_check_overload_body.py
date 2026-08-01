
def _check_overload_body(func):
    try:
        parsed_def = parse_def(func)
    except OSError:
        # Parsing the function definition can raise an OSError if source is unavailable.
        # Since this is just an initial check, just raise a warning if this is the case.
        warnings.warn(
            f"Unable to retrieve source for @torch.jit._overload function: {func}.",
            stacklevel=2,
        )
        return

    body = parsed_def.ast.body[0].body

    def is_pass(x):
        return isinstance(x, ast.Pass)

    def is_ellipsis(x):
        return (
            isinstance(x, ast.Expr)
            and isinstance(x.value, ast.Constant)
            and x.value.value is Ellipsis
        )

    if len(body) != 1 or not (is_pass(body[0]) or is_ellipsis(body[0])):
        msg = (
            "Only `pass` statement or `...` can be the body of overload declaration:\n"
        )
        msg += "\n".join(parsed_def.source.split("\n")[:3])
        msg += " <- Expecting `pass` or `...` here!\n" + _OVERLOAD_EXAMPLE
        raise RuntimeError(msg)

