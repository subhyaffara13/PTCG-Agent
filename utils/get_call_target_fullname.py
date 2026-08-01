
def get_call_target_fullname(ref: RefExpr) -> str:
    if isinstance(ref.node, TypeAlias):
        # Resolve simple type aliases. In calls they evaluate to the type they point to.
        target = get_proper_type(ref.node.target)
        if isinstance(target, Instance):
            return target.type.fullname
    return ref.fullname

