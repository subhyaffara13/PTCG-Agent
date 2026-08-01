
def _add_init(
    ctx: mypy.plugin.ClassDefContext,
    attributes: list[Attribute],
    adder: MethodAdder,
    method_name: Literal["__init__", "__attrs_init__"],
) -> None:
    """Generate an __init__ method for the attributes and add it to the class."""
    # Convert attributes to arguments with kw_only arguments at the end of
    # the argument list
    pos_args = []
    kw_only_args = []
    sym_table = ctx.cls.info.names
    for attribute in attributes:
        if not attribute.init:
            continue
        if attribute.kw_only:
            kw_only_args.append(attribute.argument(ctx))
        else:
            pos_args.append(attribute.argument(ctx))

        # If the attribute is Final, present in `__init__` and has
        # no default, make sure it doesn't error later.
        if not attribute.has_default and attribute.name in sym_table:
            sym_node = sym_table[attribute.name].node
            if isinstance(sym_node, Var) and sym_node.is_final:
                sym_node.final_set_in_init = True
    args = pos_args + kw_only_args
    if all(arg.variable.type and is_unannotated_any(arg.variable.type) for arg in args):
        # This workaround makes --disallow-incomplete-defs usable with attrs,
        # but is definitely suboptimal as a long-term solution.
        # See https://github.com/python/mypy/issues/5954 for discussion.
        for a in args:
            a.variable.type = AnyType(TypeOfAny.implementation_artifact)
            a.type_annotation = AnyType(TypeOfAny.implementation_artifact)
    adder.add_method(method_name, args, NoneType())

