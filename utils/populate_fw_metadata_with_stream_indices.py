
def populate_fw_metadata_with_stream_indices(
    gm: torch.fx.GraphModule, fw_metadata: "ViewAndMutationMeta"
) -> None:
    """
    Populates fw_metadata.mutated_inp_stream_indices with stream indices from the compiled graph.

    The forward graph outputs are structured as:
    (*mutated_inputs, *user_outputs, *intermediate_bases, *saved_tensors, *saved_symints)

    We extract the stream index for each mutated input from the graph's output node.
    """

    num_mutated_inps = fw_metadata.num_mutated_inp_runtime_indices
    if num_mutated_inps == 0:
        fw_metadata.mutated_inp_stream_indices = []
        return

    # Find the output node in the graph
    output_node = None
    for node in gm.graph.find_nodes(op="output"):
        output_node = node
        break

    if output_node is None:
        raise AssertionError(
            "No output node found in the graph when extracting stream indices"
        )

    # The output node's args[0] is a tuple/list of all outputs
    output_args = output_node.args[0]

    # Extract stream indices for the first num_mutated_inps outputs
    stream_indices = []
    for i in range(num_mutated_inps):
        if i < len(output_args):
            output_arg = output_args[i]
            # Get the stream index from the node metadata
            stream_idx = (
                get_stream(output_arg)
                if isinstance(output_arg, torch.fx.Node)
                else None
            )
            stream_indices.append(stream_idx)
        else:
            stream_indices.append(None)

    fw_metadata.mutated_inp_stream_indices = stream_indices

