
def is_view(op: torch._ops.OpOverload) -> bool:
    """
    Does this op overload have aliasing
    """
    return any(a.alias_info is not None for a in op._schema.arguments)

