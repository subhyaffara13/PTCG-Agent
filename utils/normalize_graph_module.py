
def normalize_graph_module(gm: torch.fx.GraphModule) -> None:
    for node in gm.graph.nodes:
        if node.op == "placeholder":
            node.meta["val"] = node.meta["example_value"]

