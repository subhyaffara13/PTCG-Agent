
def get_bwd_subgraph_outputs(
    subgraph_buffer: SubgraphResults,
    mask_graph_buffer: SubgraphResults,
    joint_outputs: JointOutputResult,
) -> list[ComputedBuffer | TensorBox | None]:
    subgraph_buffer = (
        subgraph_buffer if isinstance(subgraph_buffer, Sequence) else [subgraph_buffer]
    )
    mask_graph_buffer = (
        mask_graph_buffer
        if isinstance(mask_graph_buffer, Sequence)
        else [mask_graph_buffer]
    )
    joint_output_buffers = [
        joint_outputs.grad_input,
        *joint_outputs.captured_grads_compute,
        *joint_outputs.captured_grads,
        *joint_outputs.mutated_grads,
    ]

    return [*subgraph_buffer, *mask_graph_buffer, *joint_output_buffers]

