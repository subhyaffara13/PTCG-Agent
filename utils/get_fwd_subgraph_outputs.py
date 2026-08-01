
def get_fwd_subgraph_outputs(
    subgraph_buffer: SubgraphResults, mask_graph_buffer: SubgraphResults
) -> list[ComputedBuffer | None]:
    subgraph_buffer = (
        subgraph_buffer if isinstance(subgraph_buffer, Sequence) else [subgraph_buffer]
    )
    mask_graph_buffer = (
        mask_graph_buffer
        if isinstance(mask_graph_buffer, Sequence)
        else [mask_graph_buffer]
    )

    return [*subgraph_buffer, *mask_graph_buffer]

