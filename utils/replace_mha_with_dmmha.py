
def replace_mha_with_dmmha(model: OnnxModel, past_seq_len_name: str):
    # Add `beam_width` and `cache_indirection` as model inputs
    beam_width = "beam_width"
    cache_indirection = "cache_indirection"

    model.model.graph.input.extend(
        [
            onnx.helper.make_tensor_value_info(beam_width, TensorProto.INT32, shape=[1]),
            onnx.helper.make_tensor_value_info(
                cache_indirection, TensorProto.INT32, shape=["batch_size", "beam_width", "max_sequence_length"]
            ),
        ]
    )

    # Replace all `MultiHeadAttention` nodes with `DecoderMaskedMultiHeadAttention` nodes
    mha_nodes = list(filter(lambda node: node.op_type == "MultiHeadAttention", model.model.graph.node))
    for idx, node in enumerate(mha_nodes):
        # Get `num_heads` attribute from MHA
        num_heads = 0
        for att in node.attribute:
            if att.name == "num_heads":
                num_heads = att.i
                break

        # Make Q*K outputs for cross-attention layers, which happen every alternative layer
        qk_output_name = f"output_cross_qk_{idx // 2}"
        qk_output = onnx.helper.make_tensor_value_info(
            qk_output_name, TensorProto.FLOAT, shape=["batch_size", num_heads, 1, "encode_sequence_length / 2"]
        )
        if idx % 2 == 1:
            model.model.graph.output.append(qk_output)

        # Make DMMHA node
        dmmha_node = onnx.helper.make_node(
            "DecoderMaskedMultiHeadAttention",
            inputs=[
                node.input[0],  # query
                node.input[1],  # key
                node.input[2],  # value
                "",  # mask_index
                "",  # relative_position_bias
                node.input[6] if len(node.input) > 4 else "",  # past_key
                node.input[7] if len(node.input) > 4 else "",  # past_value
                past_seq_len_name,  # past_sequence_length
                beam_width,  # beam_width
                cache_indirection,  # cache_indirection
                node.input[3],  # bias
            ],
            outputs=[
                node.output[0],  # output
                node.output[1] if len(node.input) > 4 else "",  # present_key
                node.output[2] if len(node.input) > 4 else "",  # present_value
                qk_output_name if idx % 2 == 1 else "",  # output_cross_qk
            ],
            name=node.name.replace("MultiHeadAttention", "DecoderMaskedMultiHeadAttention"),
            domain="com.microsoft",
            num_heads=num_heads,
            output_qk=(idx % 2),
            past_present_share_buffer=1,
        )
        if idx % 2 == 0:
            # Remove empty string for output_cross_qk, which happens every alternative layer
            dmmha_node.output.remove("")

        model.model.graph.node.remove(node)
        model.model.graph.node.extend([dmmha_node])

    model.topological_sort()
    return model

