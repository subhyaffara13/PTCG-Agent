
def _filter_nodes_by_target(nodes: list[torch.fx.Node], target) -> list[torch.fx.Node]:
    return [x for x in nodes if x.target == target]

