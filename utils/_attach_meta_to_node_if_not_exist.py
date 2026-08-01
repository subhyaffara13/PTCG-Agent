
def _attach_meta_to_node_if_not_exist(model: GraphModule) -> None:
    """Attach meta field to all nodes of the graph if it does not exist,
    meta field is a field stores some meta information about the node, such
    as dtype and shape information for output of the node, this only exists
    if the program is captured by make_fx (used in quantize_pt2e flow), if
    the program is captured by torch.fx symbolic tracing, this field may not exist,
    so we add it here to avoid checking this all over the places
    """
    for node in model.graph.nodes:
        if not hasattr(node, "meta"):
            node.meta = {}

