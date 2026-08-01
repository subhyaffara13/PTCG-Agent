
def verify_t5_decoder_subgraph(graph: onnx.GraphProto, precision: Precision):
    """Verify T5 decoder subgraph

    Args:
        graph (onnx.GraphProto): onnx graph of T5 decoder
        precision (Precision): Precision (FLOAT16 or FLOAT32) of the model.

    Raises:
        ValueError: Number of inputs not expected.
        ValueError: Input name is not expected.
        ValueError: Input data type is not expected.
        ValueError: Number of outputs not expected.
        ValueError: Output name is not expected.
        ValueError: Output data type is not expected.
    """
    is_float16 = precision == Precision.FLOAT16.value
    float_type = TensorProto.FLOAT16 if is_float16 else TensorProto.FLOAT

    input_count = len(graph.input)
    layer_count = (input_count - 2) // 4
    assert layer_count >= 1

    # Expect inputs:
    #   input_ids: int32 (B, 1)
    #   encoder_attention_mask: int32 (B, encode_sequence_length)

    #   past_key_self_0: (B, num_heads, past_decode_sequence_length, head_size)
    #   past_value_self_0: (B, num_heads, past_decode_sequence_length, head_size)
    #   ... (for each self attention layer)

    #   past_key_cross_0: (B, num_heads, encode_sequence_length, head_size)
    #   past_value_cross_0: (B, num_heads, encode_sequence_length, head_size)
    #   ... (for each cross attention layer)

    # TODO: encoder_hidden_states is optional
    expected_inputs = ["input_ids", "encoder_attention_mask"]
    for i in range(layer_count):
        expected_inputs.append(f"past_key_self_{i}")
        expected_inputs.append(f"past_value_self_{i}")
    for i in range(layer_count):
        expected_inputs.append(f"past_key_cross_{i}")
        expected_inputs.append(f"past_value_cross_{i}")

    if len(graph.input) != len(expected_inputs):
        raise ValueError(f"Number of inputs expected to be {len(expected_inputs)}. Got {len(graph.input)}")

    for i, expected_input in enumerate(expected_inputs):
        if graph.input[i].name != expected_input:
            raise ValueError(f"Input {i} is expected to be {expected_input}. Got {graph.input[i].name}")

        expected_type = TensorProto.INT32 if i < 2 else float_type
        input_type = graph.input[i].type.tensor_type.elem_type
        if input_type != expected_type:
            raise ValueError(f"Input {i} is expected to have onnx data type {expected_type}. Got {input_type}")

    # Expect outputs:
    #   logits:               (B, 1, vocab_size)
    #   present_key_self_0:   (B, num_heads, past_decode_sequence_length + 1, head_size)
    #   present_value_self_0: (B, num_heads, past_decode_sequence_length + 1, head_size)
    #                     ... (for each self attention layer)
    expected_outputs = ["logits"]
    for i in range(layer_count):
        expected_outputs.append(f"present_key_self_{i}")
        expected_outputs.append(f"present_value_self_{i}")

    if len(graph.output) != len(expected_outputs):
        raise ValueError(f"Number of outputs expected to be {len(expected_outputs)}. Got {len(graph.output)}")

    for i, expected_output in enumerate(expected_outputs):
        if graph.output[i].name != expected_output:
            raise ValueError(f"Output {i} is expected to be {expected_output}. Got {graph.output[i].name}")
        output_type = graph.output[i].type.tensor_type.elem_type
        if output_type != float_type:
            raise ValueError(f"Output {i} is expected to have onnx data type {float_type}. Got {output_type}")

