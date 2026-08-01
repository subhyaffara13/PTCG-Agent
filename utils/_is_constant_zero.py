
def _is_constant_zero(node: str | nodes.NodeNG) -> bool:
    # We have to check that node.value is not False because node.value == 0 is True
    # when node.value is False
    return isinstance(node, nodes.Const) and node.value == 0 and node.value is not False

