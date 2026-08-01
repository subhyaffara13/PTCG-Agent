
def is_empty_dict_literal(node: nodes.NodeNG | None) -> bool:
    return isinstance(node, nodes.Dict) and not node.items

