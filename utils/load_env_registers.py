
def load_env_registers(builder: IRBuilder, prefix: str = "") -> None:
    """Load the registers for the current FuncItem being visited.

    Adds the arguments of the FuncItem to the environment. If the
    FuncItem is nested inside of another function, then this also
    loads all of the outer environments of the FuncItem into registers
    so that they can be used when accessing free variables.
    """
    add_args_to_env(builder, local=True, prefix=prefix)

    fn_info = builder.fn_info
    fitem = fn_info.fitem
    if fn_info.is_nested and builder.fn_infos[-2]._env_class is not None:
        load_outer_envs(builder, fn_info.callable_class)
        # If this is a FuncDef, then make sure to load the FuncDef into its own environment
        # class so that the function can be called recursively.
        if isinstance(fitem, FuncDef) and fn_info.add_nested_funcs_to_env:
            setup_func_for_recursive_call(builder, fitem, fn_info.callable_class, prefix=prefix)

