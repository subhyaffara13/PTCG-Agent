
def _shard_state_dict(
    state_dict: dict[str, torch.Tensor],
    placement_strategies: dict[Node, OpSpec],
    graph_signature: ExportGraphSignature,
    mesh: DeviceMesh,
) -> None:
    """
    Inplace partition the weights based on the OpSpec
    """
    for node, op_spec in placement_strategies.items():
        if node.op != "placeholder":
            continue
        if node.name in graph_signature.inputs_to_parameters:
            fqn = graph_signature.inputs_to_parameters[node.name]
        elif node.name in graph_signature.inputs_to_buffers:
            fqn = graph_signature.inputs_to_buffers[node.name]
        else:
            continue
        if fqn not in state_dict:
            raise AssertionError(f"{fqn} not found in state dict: {state_dict.keys()}")

        original_param = state_dict[fqn]
        dtensor_param = distribute_tensor(
            original_param,
            mesh,
            op_spec.output_spec.placements,
        )
        local_param = dtensor_param.to_local()
        state_dict[fqn] = (
            torch.nn.Parameter(local_param)
            if isinstance(original_param, torch.nn.Parameter)
            else local_param
        )

