
def verify_gpt2_subgraph(graph: onnx.GraphProto, precision: Precision):
    """Verify GPT-2 subgraph

    Args:
        graph (onnx.GraphProto): onnx graph of GPT-2
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

    input_count = len(graph.input)
    layer_count = input_count - 3
    assert layer_count >= 1

    expected_inputs = ["input_ids", "position_ids", "attention_mask"] + [f"past_{i}" for i in range(layer_count)]
    if len(graph.input) != len(expected_inputs):
        raise ValueError(f"Number of inputs expected to be {len(expected_inputs)}. Got {len(graph.input)}")

    for i, expected_input in enumerate(expected_inputs):
        if graph.input[i].name != expected_input:
            raise ValueError(f"Input {i} is expected to be {expected_input}. Got {graph.input[i].name}")

        expected_type = TensorProto.INT32
        if i >= 3:
            expected_type = TensorProto.FLOAT16 if is_float16 else TensorProto.FLOAT

        input_type = graph.input[i].type.tensor_type.elem_type
        if input_type != expected_type:
            raise ValueError(f"Input {i} is expected to have onnx data type {expected_type}. Got {input_type}")
    logger.info("Verifying GPT-2 graph inputs: name and data type are good.")

    expected_outputs = ["logits"] + [f"present_{i}" for i in range(layer_count)]
    if len(graph.output) != len(expected_outputs):
        raise ValueError(f"Number of outputs expected to be {len(expected_outputs)}. Got {len(graph.output)}")

    for i, expected_output in enumerate(expected_outputs):
        if graph.output[i].name != expected_output:
            raise ValueError(f"Output {i} is expected to be {expected_output}. Got {graph.output[i].name}")

        expected_type = TensorProto.FLOAT16 if is_float16 else TensorProto.FLOAT
        output_type = graph.output[i].type.tensor_type.elem_type
        if output_type != expected_type:
            raise ValueError(f"Input {i} is expected to have onnx data type {expected_type}. Got {output_type}")
    logger.info("Verifying GPT-2 graph outputs: name and data type are good.")

    # TODO(tianleiwu): verify shapes of inputs and outputs.
    return

