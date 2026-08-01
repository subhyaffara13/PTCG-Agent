
def _looks_like_dataclasses(node: nodes.Module) -> bool:
    return node.qname() == "dataclasses"

