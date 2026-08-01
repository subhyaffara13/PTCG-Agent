
def _has_tag_is_backward(node: fx.Node) -> bool:
    return node.meta.get("partitioner_tag", None) == "is_backward"

