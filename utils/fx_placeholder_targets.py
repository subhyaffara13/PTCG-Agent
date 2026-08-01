
def fx_placeholder_targets(gm: torch.fx.GraphModule) -> list[str]:
    return [n.target for n in gm.graph.nodes if n.op == "placeholder"]

