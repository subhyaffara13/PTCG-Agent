
def _is_set_grad_enabled_node(node: torch.fx.Node) -> torch.fx.Node | bool:
    return (
        node
        and node.op == "call_function"
        and node.target is torch._C._set_grad_enabled
    )

