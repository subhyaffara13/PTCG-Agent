
def add_vars_to_env(builder: IRBuilder, prefix: str = "") -> None:
    """Add relevant local variables and nested functions to the environment class.

    Add all variables and functions that are declared/defined within current
    function and are referenced in functions nested within this one to this
    function's environment class so the nested functions can reference
    them even if they are declared after the nested function's definition.
    Note that this is done before visiting the body of the function.
    """
    env_for_func: FuncInfo | ImplicitClass = builder.fn_info
    if builder.fn_info.is_generator:
        env_for_func = builder.fn_info.generator_class
    elif (
        builder.fn_info.is_nested or builder.fn_info.in_non_ext
    ) and not builder.fn_info.is_comprehension_scope:
        env_for_func = builder.fn_info.callable_class

    if builder.fn_info.fitem in builder.free_variables:
        # Sort the variables to keep things deterministic
        for var in sorted(builder.free_variables[builder.fn_info.fitem], key=lambda x: x.name):
            if isinstance(var, Var):
                rtype = builder.type_to_rtype(var.type)
                builder.add_var_to_env_class(
                    var, rtype, env_for_func, reassign=False, prefix=prefix
                )

    if builder.fn_info.fitem in builder.encapsulating_funcs:
        for nested_fn in builder.encapsulating_funcs[builder.fn_info.fitem]:
            if isinstance(nested_fn, FuncDef):
                # The return type is 'object' instead of an RInstance of the
                # callable class because differently defined functions with
                # the same name and signature across conditional blocks
                # will generate different callable classes, so the callable
                # class that gets instantiated must be generic.
                if nested_fn.is_generator or nested_fn.is_coroutine:
                    prefix = GENERATOR_ATTRIBUTE_PREFIX
                builder.add_var_to_env_class(
                    nested_fn, object_rprimitive, env_for_func, reassign=False, prefix=prefix
                )

