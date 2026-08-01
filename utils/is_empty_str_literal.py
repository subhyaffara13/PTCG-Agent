
def is_empty_str_literal(node: nodes.NodeNG | None) -> bool:
    return (
        isinstance(node, nodes.Const) and isinstance(node.value, str) and not node.value
    )

