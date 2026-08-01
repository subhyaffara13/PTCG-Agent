
def _has_tag_must_be_in_forward(node: fx.Node) -> bool:
    return node.meta.get("partitioner_tag", None) == "must_be_in_forward"

