
def setup_func_for_recursive_call(
    builder: IRBuilder, fdef: FuncDef, base: ImplicitClass, prefix: str = ""
) -> None:
    """Enable calling a nested function (with a callable class) recursively.

    Adds the instance of the callable class representing the given
    FuncDef to a register in the environment so that the function can
    be called recursively. Note that this needs to be done only for
    nested functions.
    """
    # First, set the attribute of the environment class so that GetAttr can be called on it.
    prev_env = builder.fn_infos[-2].env_class
    attr_name = prefix + fdef.name
    prev_env.attributes[attr_name] = builder.type_to_rtype(fdef.type)
    line = fdef.line

    if isinstance(base, GeneratorClass):
        # If we are dealing with a generator class, then we need to first get the register
        # holding the current environment class, and load the previous environment class from
        # there.
        prev_env_reg = builder.add(GetAttr(base.curr_env_reg, ENV_ATTR_NAME, line))
    else:
        prev_env_reg = base.prev_env_reg

    # Obtain the instance of the callable class representing the FuncDef, and add it to the
    # current environment.
    val = builder.add(GetAttr(prev_env_reg, attr_name, line))
    target = builder.add_local_reg(fdef, object_rprimitive)
    builder.assign(target, val, line)

