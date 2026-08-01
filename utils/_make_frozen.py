
def _make_frozen(ctx: mypy.plugin.ClassDefContext, attributes: list[Attribute]) -> None:
    """Turn all the attributes into properties to simulate frozen classes."""
    for attribute in attributes:
        if attribute.name in ctx.cls.info.names:
            # This variable belongs to this class so we can modify it.
            node = ctx.cls.info.names[attribute.name].node
            if not isinstance(node, Var):
                # The superclass attribute was overridden with a non-variable.
                # No need to do anything here, override will be verified during
                # type checking.
                continue
            node.is_property = True
        else:
            # This variable belongs to a super class so create new Var so we
            # can modify it.
            var = Var(attribute.name, attribute.init_type)
            var.info = ctx.cls.info
            var._fullname = f"{ctx.cls.info.fullname}.{var.name}"
            ctx.cls.info.names[var.name] = SymbolTableNode(MDEF, var)
            var.is_property = True

