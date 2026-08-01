
def serialize_graph_module(gm: torch.fx.GraphModule) -> SerializedGraphModule:
    # NOTE: mutates the graph module
    gm.meta = {}
    for node in gm.graph.nodes:
        # pyrefly: ignore [implicit-any]
        node.meta = {}
    return SerializedGraphModule(gm)

