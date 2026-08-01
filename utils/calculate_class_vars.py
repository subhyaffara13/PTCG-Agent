
def calculate_class_vars(info: TypeInfo) -> None:
    """Try to infer additional class variables.

    Subclass attribute assignments with no type annotation are assumed
    to be classvar if overriding a declared classvar from the base
    class.

    This must happen after the main semantic analysis pass, since
    this depends on base class bodies having been fully analyzed.
    """
    for name, sym in info.names.items():
        node = sym.node
        if isinstance(node, Var) and node.info and node.is_inferred and not node.is_classvar:
            for base in info.mro[1:]:
                member = base.names.get(name)
                if member is not None and isinstance(member.node, Var) and member.node.is_classvar:
                    node.is_classvar = True

