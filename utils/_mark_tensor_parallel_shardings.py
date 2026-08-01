
def _mark_tensor_parallel_shardings(
    gm: GraphModule,
    graph_signature: ExportGraphSignature,
    mesh: DeviceMesh,
    parameter_placements: dict[str, Placement],
) -> dict[Node, OpSpec]:
    """
    Mark the placement strategies of the parameter and buffer placeholder nodes.
    """
    placement_strategies: dict[Node, OpSpec] = {}
    num_params_and_buffers = len(graph_signature.inputs_to_parameters) + len(
        graph_signature.inputs_to_buffers
    )
    placeholder_idx: int = 0
    for node in gm.graph.nodes:
        if node.op == "placeholder":
            if placeholder_idx < num_params_and_buffers:
                fqn: str = _get_input_node_fqn(node.name, graph_signature)
                placement: Placement = (
                    parameter_placements[fqn]
                    if fqn in parameter_placements
                    else Replicate()
                )
                placement_strategies[node] = _create_placement_strategy(
                    node,
                    mesh,
                    placements=(placement,),
                )
                placeholder_idx += 1
            else:
                placement_strategies[node] = _create_placement_strategy(
                    node,
                    mesh,
                    placements=(Replicate(),),
                )
    return placement_strategies

