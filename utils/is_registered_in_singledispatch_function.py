
def is_registered_in_singledispatch_function(node: nodes.FunctionDef) -> bool:
    """Check if the given function node is a singledispatch function."""
    singledispatch_qnames = (
        "functools.singledispatch",
        "singledispatch.singledispatch",
    )

    if not isinstance(node, nodes.FunctionDef):
        return False

    decorators = node.decorators.nodes if node.decorators else []
    for decorator in decorators:
        # func.register are function calls or register attributes
        # when the function is annotated with types
        match decorator:
            case nodes.Call(func=func) | (nodes.Attribute() as func):
                pass
            case _:
                continue

        if not (isinstance(func, nodes.Attribute) and func.attrname == "register"):
            continue

        try:
            func_def = next(func.expr.infer())
        except astroid.InferenceError:
            continue

        if isinstance(func_def, nodes.FunctionDef):
            return decorated_with(func_def, singledispatch_qnames)

    return False

