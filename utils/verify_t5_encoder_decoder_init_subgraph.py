
def verify_t5_encoder_decoder_init_subgraph(graph: onnx.GraphProto, precision: Precision):
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
    new_format = "cross" in graph.output[0].name

    # Expect 3 inputs:
    #   encoder_input_ids:      int32 (B, encode_sequence_length)
    #   encoder_attention_mask: int32 (B, encode_sequence_length)
    #   decoder_input_ids:      int32 (B, 1)
    expected_inputs = [
        "encoder_input_ids",
        "encoder_attention_mask",
        "decoder_input_ids",
    ]
    if new_format:
        expected_inputs = expected_inputs[:2]
    if len(graph.input) != len(expected_inputs):
        raise ValueError(f"Number of inputs expected to be {len(expected_inputs)}. Got {len(graph.input)}")

    for i, expected_input in enumerate(expected_inputs):
        if graph.input[i].name != expected_input:
            raise ValueError(f"Input {i} is expected to be {expected_input}. Got {graph.input[i].name}")

        expected_type = TensorProto.INT32
        input_type = graph.input[i].type.tensor_type.elem_type
        if input_type != expected_type:
            raise ValueError(f"Input {i} is expected to have onnx data type {expected_type}. Got {input_type}")

    if new_format:
        assert len(graph.output) % 2 == 0
        layer_count = len(graph.output) // 2
        assert layer_count >= 1

        # Expected outputs:
        #   present_key_cross_0:   (B, num_heads, encode_sequence_length, head_size)
        #   present_value_cross_0: (B, num_heads, encode_sequence_length, head_size)
        #                      ... (for each cross attention layer)
        expected_outputs = []
        for i in range(layer_count):
            expected_outputs.append(f"present_key_cross_{i}")
            expected_outputs.append(f"present_value_cross_{i}")
    else:
        logger.warning("This format is deprecated. Please export T5 encoder in new format with only cross outputs.")
        assert (len(graph.output) - 2) % 4 == 0
        layer_count = (len(graph.output) - 2) // 4
        assert layer_count >= 1

        # Expected outputs:
        #   logits:                (B, 1, vocab_size)
        #   encoder_hidden_states: (B, encode_sequence_length, encoder_hidden_size)
        #   present_key_self_0:    (B, num_heads, 1, head_size)
        #   present_value_self_0:  (B, num_heads, 1, head_size)
        #                      ... (for each self attention layer)
        #   present_key_cross_0:   (B, num_heads, encode_sequence_length, head_size)
        #   present_value_cross_0: (B, num_heads, encode_sequence_length, head_size)
        #                      ... (for each cross attention layer)
        expected_outputs = ["logits", "encoder_hidden_states"]
        for i in range(layer_count):
            expected_outputs.append(f"present_key_self_{i}")
            expected_outputs.append(f"present_value_self_{i}")
        for i in range(layer_count):
            expected_outputs.append(f"present_key_cross_{i}")
            expected_outputs.append(f"present_value_cross_{i}")

    if len(graph.output) != len(expected_outputs):
        raise ValueError(f"Number of outputs expected to be {len(expected_outputs)}. Got {len(graph.output)}")

    for i, expected_output in enumerate(expected_outputs):
        if graph.output[i].name != expected_output:
            raise ValueError(f"Output {i} is expected to be {expected_output}. Got {graph.output[i].name}")

        expected_type = TensorProto.FLOAT16 if is_float16 else TensorProto.FLOAT
        output_type = graph.output[i].type.tensor_type.elem_type
        if output_type != expected_type:
            raise ValueError(f"Output {i} is expected to have onnx data type {expected_type}. Got {output_type}")

    logger.info("T5 encoder graph verified: name and data type of inputs and outputs are good.")

