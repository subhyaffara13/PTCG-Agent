
def has_nested_func_self_reference(builder: IRBuilder, fitem: FuncItem) -> bool:
    """Does a nested function contain a self-reference in its body?

    If a nested function only has references in the surrounding function,
    we don't need to add it to the environment.
    """
    if any(isinstance(sym, FuncBase) for sym in builder.free_variables.get(fitem, set())):
        return True
    return any(
        has_nested_func_self_reference(builder, nested)
        for nested in builder.encapsulating_funcs.get(fitem, [])
    )

