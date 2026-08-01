
def _check_valid_autocast_block(
    enter_autocast_node: torch.fx.Node, exit_autocast_node: torch.fx.Node
) -> None:
    if not _is_enter_autocast_node(enter_autocast_node):
        raise AssertionError(
            f"expected enter_autocast node, got {enter_autocast_node.target}"
        )
    if not _is_exit_autocast_node(exit_autocast_node):
        raise AssertionError(
            f"expected exit_autocast node, got {exit_autocast_node.target}"
        )
    if exit_autocast_node.args[0] != enter_autocast_node:
        raise AssertionError(
            "exit_autocast_node.args[0] must match enter_autocast_node"
        )

