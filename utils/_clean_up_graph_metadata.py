
def _clean_up_graph_metadata(gm: torch.fx.GraphModule) -> None:
    """
    Clean up the graph by removing sharding and partitioning related metadata
    """
    for node in gm.graph.nodes:
        if "sharding" in node.meta:
            del node.meta["sharding"]
        if "val" in node.meta and isinstance(node.meta["val"], torch.Tensor):
            local_tensor_meta = _extract_tensor_metadata(node.meta["val"])
            node.meta["tensor_meta"] = local_tensor_meta

