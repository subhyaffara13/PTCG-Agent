
def get_func_target(builder: IRBuilder, fdef: FuncDef) -> AssignmentTarget:
    """Given a FuncDef, return the target for the instance of its callable class.

    If the function was not already defined somewhere, then define it
    and add it to the current environment.
    """
    if orig := fdef.original_def:
        if isinstance(orig, Decorator):
            orig = orig.func
        # Get the target associated with the previously defined FuncDef.
        return builder.lookup(orig)

    if builder.fn_info.is_generator or builder.fn_info.add_nested_funcs_to_env:
        return builder.lookup(fdef)

    return builder.add_local_reg(fdef, object_rprimitive)

