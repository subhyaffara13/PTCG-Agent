
def update_decoder_subgraph_share_buffer_and_use_decoder_masked_mha(subg: ModelProto):
    input_self_past_0 = 1
    # w/wo attention mask, w/wo hidden_state
    graph_input_names = [gi.name for gi in subg.input]
    while input_self_past_0 < 3 and not graph_input_names[input_self_past_0].startswith("past"):
        input_self_past_0 += 1
    output_self_past_0 = 1

    num_layers = int((len(subg.input) - input_self_past_0) / 4)
    input_cross_past_0 = 2 * num_layers + input_self_past_0

    new_nodes = []
    old_nodes = []
    for node in subg.node:
        if node.op_type == "MultiHeadAttention":
            old_nodes.extend([node])

    # If not all the MultiHeadAttention nodes are fused, this optimization is not applicable
    if len(old_nodes) < num_layers:
        return False

    # Redirect the RelativePositionBias node's input from past_key_self_0.shape[2] to past_sequence_length.
    # There is only one RelativePositionBias node in T5 decoder subgraph.
    rel_pos_bias_node = None
    for node in subg.node:
        if node.op_type == "RelativePositionBias":
            rel_pos_bias_node = node
            break

    decoder_masked_attention_supported_attr = [
        "past_present_share_buffer",
        "num_heads",
        "scale",
        "mask_filter_value",
        "domain",
    ]

    target_squeezed_past_seq_name = "past_sequence_length_squeezed_int64"
    tensor_names_to_rename, nodes_to_remove = find_past_seq_len_usage(subg)
    if len(tensor_names_to_rename) > 0:
        for name_to_rename in tensor_names_to_rename:
            print(f"Found tensor name `{name_to_rename}` to be renamed to `{target_squeezed_past_seq_name}`")
        for nr in nodes_to_remove:
            print(f"Found node to remove: type = {nr.op_type}, name = {nr.name}")

        squeeze_node = onnx.helper.make_node(
            "Squeeze",
            ["past_sequence_length"],
            ["past_sequence_length_squeezed"],
            name="node_past_sequence_length_squeeze",
        )
        cast_node = onnx.helper.make_node(
            "Cast",
            ["past_sequence_length_squeezed"],
            [target_squeezed_past_seq_name],
            name="node_past_sequence_length_squeeze_cast",
            to=TensorProto.INT64,
        )
        new_nodes.extend([squeeze_node, cast_node])

    for node in subg.node:
        if len(node.output) > 0 and rel_pos_bias_node is not None and node.output[0] == rel_pos_bias_node.input[1]:
            cast_node = onnx.helper.make_node(
                "Cast",
                ["past_sequence_length"],
                ["past_sequence_length_int64"],
                name="past_sequence_length_cast",
                to=TensorProto.INT64,
            )
            node.input[1] = cast_node.output[0]
            new_nodes.extend([cast_node])

        if node.op_type == "MultiHeadAttention":
            kwargs = kwargs_of(node)
            for k in kwargs.copy():
                if k not in decoder_masked_attention_supported_attr:
                    del kwargs[k]

            # note: This logic only apply to T5 model where there is no bias in Attention node.
            nis = [
                node.input[0],  # query
                node.input[1],  # key
                node.input[2],  # value
            ]

            nis.extend([node.input[4] if len(node.input) > 4 else ""])  # 2D mask
            nis.extend([node.input[5] if len(node.input) > 5 else ""])  # attention_bias
            nis.extend([node.input[6] if len(node.input) > 6 else ""])  # past_key
            nis.extend([node.input[7] if len(node.input) > 7 else ""])  # past_value
            nis.extend(["past_sequence_length"])  # past_sequence_length
            nis.extend(["beam_width"])  # beam_width
            nis.extend(["cache_indirection"])  # cache_indirection
            nis.extend([node.input[3] if len(node.input) > 3 else ""])  # bias

            kwargs["past_present_share_buffer"] = 1

            node = onnx.helper.make_node(  # noqa: PLW2901
                "DecoderMaskedMultiHeadAttention",
                nis,
                node.output,
                name=node.name,
                **kwargs,
            )

        if node not in nodes_to_remove:
            for index, name in enumerate(node.input):
                if name in tensor_names_to_rename:
                    node.input[index] = target_squeezed_past_seq_name
            new_nodes.extend([node])

    subg.ClearField("node")
    subg.node.extend(new_nodes)
    orig_input_names = [inp.name for inp in subg.input]

    new_inputs = []
    for i, vi in enumerate(subg.input):
        if i >= input_self_past_0 and i < input_cross_past_0:
            shape = shape_of(vi)
            vi = onnx.helper.make_tensor_value_info(  # noqa: PLW2901
                vi.name,
                elem_type=vi.type.tensor_type.elem_type,
                shape=[shape[0], shape[1], "max_seq_len", shape[3]],
            )
        new_inputs.extend([vi])
    if "past_sequence_length" not in orig_input_names:
        new_inputs.extend(
            [onnx.helper.make_tensor_value_info("past_sequence_length", onnx.TensorProto.INT32, shape=[1])]
        )
    if "beam_width" not in orig_input_names:
        new_inputs.extend([onnx.helper.make_tensor_value_info("beam_width", onnx.TensorProto.INT32, shape=[1])])
    if "cache_indirection" not in orig_input_names:
        new_inputs.extend(
            [
                onnx.helper.make_tensor_value_info(
                    "cache_indirection",
                    onnx.TensorProto.INT32,
                    shape=["batch_size", "beam_width", "max_seq_len"],
                )
            ]
        )
    subg.ClearField("input")
    subg.input.extend(new_inputs)

    new_outputs = []
    for i, vi in enumerate(subg.output):
        if i >= output_self_past_0:
            shape = shape_of(vi)
            vi = onnx.helper.make_tensor_value_info(  # noqa: PLW2901
                vi.name,
                elem_type=vi.type.tensor_type.elem_type,
                shape=[shape[0], shape[1], "max_seq_len", shape[3]],
            )
        new_outputs.extend([vi])
    subg.ClearField("output")
    subg.output.extend(new_outputs)

    return True

