
def _has_tag_is_forward(node: fx.Node) -> bool:
    return node.meta.get("partitioner_tag", None) == "is_forward"

