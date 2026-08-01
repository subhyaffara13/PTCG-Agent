
def is_singleton_const(node: nodes.NodeNG) -> bool:
    return isinstance(node, nodes.Const) and any(
        node.value is value for value in SINGLETON_VALUES
    )

