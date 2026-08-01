
def _is_dataclasses_decorator(node: Node) -> bool:
    if isinstance(node, CallExpr):
        node = node.callee
    if isinstance(node, RefExpr):
        return node.fullname in dataclass_makers
    return False

