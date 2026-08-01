
def is_load_tensor_node(node: fx.Node) -> bool:
    return (
        node.op == "call_function"
        and node.target is torch.ops.debugprims.load_tensor.default
    )

