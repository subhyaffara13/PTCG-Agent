
def _positional_parameters(method: nodes.FunctionDef) -> list[nodes.AssignName]:
    positional = method.args.args
    if method.is_bound() and method.type in {"classmethod", "method"}:
        positional = positional[1:]
    return positional  # type: ignore[no-any-return]

