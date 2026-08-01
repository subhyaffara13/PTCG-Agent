
def annotate_orig_fx_with_snodes(
    gm: torch.fx.GraphModule,
    snodes: SchedulerNodeList,
) -> None:
    """
    Creates a FX Graph from a list of SchedulerNode objects.
    """
    node_name_to_buf_name: dict[str, str] = {}
    update_orig_fx_node_name_to_buf_name(snodes, node_name_to_buf_name)
    if node_name_to_buf_name is None:
        return
    node_name_to_buf_meta = get_node_name_to_buf_meta(node_name_to_buf_name)
    for node in gm.graph.nodes:
        if node.name in node_name_to_buf_meta:
            node.meta["buf_meta"] = node_name_to_buf_meta.get(node.name)

