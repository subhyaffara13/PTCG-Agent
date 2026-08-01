
def is_getitem_of_multi_output(node: fx.Node) -> bool:
    if node.target != operator.getitem:
        return False
    parent = node.args[0]
    if type(parent) is not fx.Node:
        raise AssertionError(f"expected parent to be fx.Node, got {type(parent)}")
    return "tensor_meta" not in parent.meta and node.op == "call_function"

