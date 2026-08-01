
def _must_be_in_backward(node: fx.Node) -> bool:
    if _has_tag_must_be_in_backward(node):
        return True
    is_mutable = (
        isinstance(node.target, torch._ops.OpOverload)
        and node.target._schema.is_mutable
    )
    return _has_tag_is_backward(node) and is_mutable

