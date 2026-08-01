
def _has_none_qconfig(
    node: Argument, node_name_to_qconfig: dict[str, QConfigAny]
) -> bool:
    """Check if a node has a qconfig of None, i.e. user requested to not quantize
    the node
    """
    return (
        isinstance(node, Node)
        and node.name in node_name_to_qconfig
        and node_name_to_qconfig[node.name] is None
    )

