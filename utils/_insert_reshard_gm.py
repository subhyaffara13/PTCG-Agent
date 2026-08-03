import copy

def _insert_reshard_gm(
    gm: torch.fx.GraphModule,
    node: Node,
    input_arg: Node,
    input_arg_spec: DTensorSpec,
    desired_spec: DTensorSpec,
) -> None:
    """
    Transform the graph for tensor redistribution.
    """
    input_arg_spec.tensor_meta = input_arg.meta["tensor_meta"]
    desired_spec.tensor_meta = input_arg.meta["tensor_meta"]
    input_arg_tensor = input_arg.meta["val"]

    # insert reshard operation
    def reshard_fn(local_tensor: torch.Tensor) -> torch.Tensor:
        return redistribute_local_tensor(
            local_tensor,
            input_arg_spec,
            desired_spec,
        )

    reshard_gm = make_fx(reshard_fn)(input_arg_tensor)
    reshard_gm_nodes = list(reshard_gm.graph.nodes)
    input_node = reshard_gm_nodes[0]
    with gm.graph.inserting_before(node):
        # copy nn_module_stack metadata for output, all-reduce nodes
        for reshard_node in reshard_gm.graph.nodes:
            if reshard_node.op not in ["placeholder", "output"]:
                reshard_node.meta["nn_module_stack"] = (
                    copy.copy(input_arg.meta["nn_module_stack"])
                    if input_arg.op != "placeholder"
                    else copy.copy(node.meta["nn_module_stack"])
                )
        output_node = gm.graph.graph_copy(
            reshard_gm.graph,
            val_map={
                input_node: input_arg,
            },
        )
    node.replace_input_with(input_arg, output_node)  # type: ignore[arg-type]

