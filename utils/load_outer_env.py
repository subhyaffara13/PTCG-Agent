
def load_outer_env(
    builder: IRBuilder, base: Value, outer_env: dict[SymbolNode, SymbolTarget]
) -> Value:
    """Load the environment class for a given base into a register.

    Additionally, iterates through all of the SymbolNode and
    AssignmentTarget instances of the environment at the given index's
    symtable, and adds those instances to the environment of the
    current environment. This is done so that the current environment
    can access outer environment variables without having to reload
    all of the environment registers.

    Returns the register where the environment class was loaded.
    """
    env = builder.add(GetAttr(base, ENV_ATTR_NAME, builder.fn_info.fitem.line))
    assert isinstance(env.type, RInstance), f"{env} must be of type RInstance"

    for symbol, target in outer_env.items():
        attr_name = symbol.name
        if isinstance(target, AssignmentTargetAttr):
            attr_name = target.attr
        env.type.class_ir.attributes[attr_name] = target.type
        symbol_target = AssignmentTargetAttr(env, attr_name)
        builder.add_target(symbol, symbol_target)

    return env

