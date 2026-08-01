
def merge_unbind_stack(match: Match, unbind_input: torch.fx.Node, dim: int):
    unbind_node = next(node for node in match.nodes if node.target is torch.unbind)
    UnbindCatRemover().remove_unbind(match.graph, unbind_node)

