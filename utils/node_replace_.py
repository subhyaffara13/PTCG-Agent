
def node_replace_(old_node: torch.fx.Node, new_node: torch.fx.Node) -> None:
    """
    Replace all uses of old_node with new_node.
    """
    old_node.replace_all_uses_with(new_node)
    old_node.users.clear()
    old_node.graph.erase_node(old_node)

