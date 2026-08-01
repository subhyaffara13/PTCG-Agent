
def _recursive_record_user_visible_output_idxs(gm: GraphModule) -> None:
    # invoke_subgraph HOP requires output strides to be respected
    for node in gm.graph.find_nodes(
        op="call_function", target=torch.ops.higher_order.invoke_subgraph
    ):
        subgraph = getattr(gm, node.args[0].target)

        for node in subgraph.graph.find_nodes(op="output"):
            node.meta["user_visible_output_idxs"] = [
                idx
                for idx in range(len(node.args[0]))
                if isinstance(node.args[0][idx], torch.fx.Node)
            ]
        _recursive_record_user_visible_output_idxs(subgraph)

