
def is_registered_in_singledispatchmethod_function(node: nodes.FunctionDef) -> bool:
    """Check if the given function node is a singledispatchmethod function."""
    singledispatchmethod_qnames = (
        "functools.singledispatchmethod",
        "singledispatch.singledispatchmethod",
    )

    decorators = node.decorators.nodes if node.decorators else []
    for decorator in decorators:
        func_def = find_inferred_fn_from_register(decorator)
        if func_def:
            return decorated_with(func_def, singledispatchmethod_qnames)

    return False

