
def add_output_qk_to_mha(model: OnnxModel, dtype: int = 0, skip_node_idxs: list[int] = []):  # noqa: B006
    # Add output_qk as output to MultiHeadAttention ops and as outputs to model
    output_qk_basename = "output_cross_qk"
    output_qks = []
    mha_nodes = list(filter(lambda node: node.op_type == "MultiHeadAttention", model.model.graph.node))
    for idx, node in enumerate(mha_nodes):
        # Skip MHA nodes where output_qk does not need to be added
        if idx in skip_node_idxs:
            continue

        # Get `num_heads` attribute from MHA
        num_heads = 0
        for att in node.attribute:
            if att.name == "num_heads":
                num_heads = att.i
                break

        # Get dtype for `output_qk` based on MHA bias if not provided
        output_qk_dtype = dtype
        if output_qk_dtype == 0:
            for i in model.model.graph.initializer:
                if i.name == node.input[3]:
                    output_qk_dtype = i.data_type
                    break

        # Get `target_sequence_length` attribute from 4D input for key if it's a constant
        target_sequence_length = "target_sequence_length"
        for i in model.model.graph.input:
            if i.name == node.input[1]:
                target_sequence_length = i.type.tensor_type.shape.dim[2].dim_value
                break

        # MHA op takes the following potential outputs:
        # output, present_key, present_value
        while len(node.output) < 3:
            node.output.append("")

        output_qk_name = f"{output_qk_basename}_{idx // 2}"
        node.output.append(output_qk_name)
        output_qks.append(
            onnx.helper.make_tensor_value_info(
                output_qk_name,
                output_qk_dtype,
                shape=["batch_size", num_heads, "sequence_length", target_sequence_length],
            ),
        )

    model.model.graph.output.extend(output_qks)
    model.topological_sort()
    return model

