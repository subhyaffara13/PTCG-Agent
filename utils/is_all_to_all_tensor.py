
def is_all_to_all_tensor(node: torch.fx.Node) -> bool:
    return (
        node.op == "call_function"
        and node.target is torch.ops._c10d_functional.all_to_all_single.default
    )

