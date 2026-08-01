
def _recursive_record_original_output_strides(gm: GraphModule) -> None:
    # invoke_subgraph HOP requires output strides to be respected
    for node in gm.graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.invoke_subgraph
    ):
        subgraph = getattr(gm, node.args[0].target)
        _recursive_record_original_output_strides(subgraph)

    record_original_output_strides(gm)

