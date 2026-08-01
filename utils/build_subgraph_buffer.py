
def build_subgraph_buffer(
    args: list[TensorBox],
    subgraph: Subgraph,
):
    """
    This function is adapted from ../kernel/flex_attention.py.
    The goal is to take in the required args and produce the subgraph buffer
    The subgraph buffer is a ComputedBuffer that will be inlined into the triton template

    Args:
        args: The args that are passed into the subgraph
        subgraph: The Subgraph ir for which to produce the output node
    """
    cnt = 0
    env = {}
    for node in subgraph.graph_module.graph.nodes:
        if node.op == "placeholder":
            env[node] = args[cnt]
            cnt += 1
        elif node.op == "call_function":
            # For call_function we use the default lowerings and pass in the
            # already created TensorBoxes as args
            args, kwargs = tree_map(lambda x: env.get(x, x), (node.args, node.kwargs))
            env[node] = lowerings[node.target](*args, **kwargs)
        elif node.op == "output":

            def convert_output_node_to_buffer(output):
                if output is None:
                    return None
                output_node = output
                output_buffer = env[output_node]
                assert isinstance(output_buffer, TensorBox), (
                    "The output node for B2B-GEMM's subgraph must be a TensorBox, but got: ",
                    type(output_buffer),
                )
                assert isinstance(output_buffer.data, StorageBox), (
                    "The output node for B2B-GEMM's subgraph must be a StorageBox, but got: ",
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

            # node.args[0] should be a single element representing the output of the subgraph
            return tree_map(convert_output_node_to_buffer, node.args[0])

    raise ValueError("B2B-GEMM was passed a subgraph with no output node!")


def build_subgraph_buffer(args: list[TensorBox], subgraph: Subgraph) -> SubgraphResults:
    return build_subgraph_module_buffer(args, subgraph.graph_module)

