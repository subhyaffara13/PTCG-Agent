
def is_bwd_node(node: Node) -> bool:
    tag = node.meta.get("partitioner_tag")
    return tag == "is_backward" or tag == "must_be_in_backward"

