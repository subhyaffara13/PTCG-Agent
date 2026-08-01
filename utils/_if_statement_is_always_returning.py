
def _if_statement_is_always_returning(
    if_node: nodes.If, returning_node_class: nodes.NodeNG
) -> bool:
    return any(isinstance(node, returning_node_class) for node in if_node.body)

