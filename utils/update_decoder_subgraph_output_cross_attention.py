
def update_decoder_subgraph_output_cross_attention(subg: GraphProto):
    input_self_past_0 = 1
    # w/wo attention mask, w/wo hidden_state
    graph_input_names = [gi.name for gi in subg.input]
    while input_self_past_0 < 3 and not graph_input_names[input_self_past_0].startswith("past"):
        input_self_past_0 += 1
    output_self_present_0 = 1

    num_layers = (len(subg.output) - output_self_present_0) // 2
    input_cross_past_0 = 2 * num_layers + input_self_past_0
    past_key_cross_inputs = {subg.input[layer * 2 + input_cross_past_0].name: layer for layer in range(num_layers)}
    print(f"    -- past_key_cross_inputs = {past_key_cross_inputs}")

    input_past_key_cross_0_shape = shape_of(subg.input[input_cross_past_0])
    print(f"past_key_cross_0_shape is {input_past_key_cross_0_shape}")
    batch_size_dim = input_past_key_cross_0_shape[0]
    num_heads_dim = input_past_key_cross_0_shape[1]
    cross_seq_len_dim = input_past_key_cross_0_shape[2]

    num_layer_output_qk = 0
    for node in subg.node:
        if (node.op_type == "DecoderMaskedMultiHeadAttention") and (node.input[1] in past_key_cross_inputs):
            print(f"    -- add cross QK output from: node: {node.name} with output: {node.output}")
            num_layer_output_qk += 1
            layer = past_key_cross_inputs[node.input[1]]
            cross_attention_out_name = f"output_cross_qk_{layer}"
            appended_names = [""] * (3 - len(node.output))
            appended_names.append(cross_attention_out_name)
            node.output.extend(appended_names)
            node.attribute.extend([onnx.helper.make_attribute("output_qk", 1)])

            cross_attention = onnx.helper.make_tensor_value_info(
                cross_attention_out_name,
                TensorProto.FLOAT,
                [batch_size_dim, num_heads_dim, 1, cross_seq_len_dim],
            )
            subg.output.extend([cross_attention])
    if num_layer_output_qk != num_layers:
        raise ValueError(f"Did not add cross QK for all layers{num_layers} vs {num_layer_output_qk}")

