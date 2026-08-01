
def build_subgraph_module_buffer(
    args: list[TensorBox],
    graph_module: torch.fx.GraphModule,
) -> SubgraphResults:
    """This function's goal is to take in the required args and produce the subgraph buffer
    The subgraph buffer is a ComputedBuffer that will be inlined into the triton template

    Args:
        args: The args that are passed into the subgraph. Contains both fixed and lifted inputs.
        subgraph: The Subgraph ir for which to produce the output node
    """
    # This one we gotta keep lazy
    from ...subgraph_lowering import PointwiseSubgraphLowering

    pw_subgraph = PointwiseSubgraphLowering(
        graph_module,
        root_graph_lowering=V.graph,
        allowed_mutations=OrderedSet([torch.ops.flex_lib.zeros_and_scatter.default]),
        additional_lowerings={
            torch.ops.flex_lib.zeros_and_scatter.default: zeros_and_scatter_lowering
        },
    )
    with V.set_graph_handler(pw_subgraph):  # type: ignore[arg-type]
        pw_subgraph.run(*args)

    def convert_output_node_to_buffer(output_buffer) -> ComputedBuffer | None:
        if output_buffer is None:
            return None
        if isinstance(output_buffer, ComputedBuffer):
            # These nodes are coming from the output of zeros_and_scatter
            return output_buffer
        assert isinstance(output_buffer, TensorBox), (
            "The output node for flex attention's subgraph must be a TensorBox, but got: ",
            type(output_buffer),
        )
        assert isinstance(output_buffer.data, StorageBox), (
            "The output node for the flex attention subgraph must be a StorageBox, but got: ",
            type(output_buffer),
        )
        device = output_buffer.data.get_device()
        assert device is not None
        subgraph_buffer = ComputedBuffer(
            name=None,
            layout=FlexibleLayout(
                device=device,
                dtype=output_buffer.data.get_dtype(),
                size=output_buffer.data.get_size(),
            ),
            data=output_buffer.data.data,  # type: ignore[arg-type]
        )
        return subgraph_buffer

    return tree_map(convert_output_node_to_buffer, pw_subgraph.graph_outputs)

