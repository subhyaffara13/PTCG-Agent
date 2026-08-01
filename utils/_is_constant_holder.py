
def _is_constant_holder(spec: "TreeSpec") -> bool:
    """Checks if the spec is from a pytree registered with register_constant"""
    return isinstance(spec._context, ConstantNode)

