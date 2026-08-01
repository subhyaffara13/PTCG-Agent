
def _is_exit_autocast_node(node: torch.fx.Node) -> torch.fx.Node | bool:
    return (
        node
        and node.op == "call_function"
        and node.target is torch.amp.autocast_mode._exit_autocast
    )

