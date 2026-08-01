
def fx_placeholder_vals(gm: torch.fx.GraphModule) -> list[object]:
    return [n.meta["val"] for n in gm.graph.nodes if n.op == "placeholder"]

