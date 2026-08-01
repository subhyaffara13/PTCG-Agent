
def create_longformer_inputs(onnx_model, batch_size, sequence_length, global_length, samples):
    """Create dummy inputs for Longformer model.

    Args:
        onnx_model (OnnxModel): ONNX model
        batch_size (int): batch size
        sequence_length (int): sequence length
        global_length (int): number of global tokens
        samples (int): number of samples

    Raises:
        RuntimeError: symbolic is not supported. Use the tool convert_longformer_to_onnx.py to export ONNX model instead.

    Returns:
        List[Dict]: list of inputs
    """
    symbols = {"batch_size": batch_size, "sequence_length": sequence_length}

    dummy_inputs = {}
    for graph_input in onnx_model.get_graph_inputs_excluding_initializers():
        shape = get_shape_from_type_proto(graph_input.type)
        for i, dim in enumerate(shape):
            if isinstance(dim, str):
                if dim not in symbols:
                    raise RuntimeError(f"symbol is not supported: {dim}")
                else:
                    shape[i] = symbols[dim]

        elem_type = graph_input.type.tensor_type.elem_type
        assert elem_type in [TensorProto.FLOAT, TensorProto.INT32, TensorProto.INT64]
        data_type = (
            numpy.float32
            if elem_type == TensorProto.FLOAT
            else (numpy.int64 if elem_type == TensorProto.INT64 else numpy.int32)
        )

        if "global" in graph_input.name:
            data = numpy.zeros(shape, dtype=data_type)
            data[:, :global_length] = 1
        else:
            data = numpy.ones(shape, dtype=data_type)
        dummy_inputs[graph_input.name] = data

    all_inputs = [dummy_inputs for _ in range(samples)]
    return all_inputs

