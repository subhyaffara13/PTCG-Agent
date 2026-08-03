import math


def pad_weights_of_logits_matmul(onnx_path: str, use_external_data_format: bool = True) -> bool:
    """Pad the logits MatMul weight in the provided decoder model, which will be overwritten.

    Args:
        onnx_path (str): Path of onnx model
        use_external_data_format(bool): output tensors to external data or not.
    """
    decoder_model_proto = onnx.load_model(onnx_path, load_external_data=True)

    logits_output_name = decoder_model_proto.graph.output[0].name

    decoder_model = OnnxModel(decoder_model_proto)

    output_name_to_node = decoder_model.output_name_to_node()
    assert logits_output_name in output_name_to_node

    matmul_node = output_name_to_node[logits_output_name]
    # Sanity check - the logits need to be produced by a MatMul node
    if matmul_node.op_type != "MatMul":
        return False

    # The logits MatMul weight MUST be an initializer (or)
    # it MUST be flowing through a Transpose whose input is
    # an initializer
    pad_along_axis_1 = True
    logits_weight = decoder_model.get_initializer(matmul_node.input[1])
    if logits_weight is None:
        transpose_before_matmul = decoder_model.match_parent(matmul_node, "Transpose", 1)

        if transpose_before_matmul is None:
            return False

        logits_weight = decoder_model.get_initializer(transpose_before_matmul.input[0])

        if logits_weight is None:
            return False

        pad_along_axis_1 = False

    # The logits MatMul weight MUST be fp16
    if logits_weight.data_type != TensorProto.DataType.FLOAT16:
        return False

    # The logits MatMul weight MUST be 2-dimensional
    if len(logits_weight.dims) != 2:
        return False

    # Pad and over-write the initializer (if needed)
    actual_vocab_size = logits_weight.dims[1]

    if (actual_vocab_size % 8) == 0:
        # Already "padded"
        return True

    padded_vocab_size = math.ceil(actual_vocab_size / 8) * 8
    padding = padded_vocab_size - actual_vocab_size

    # TODO(hasesh): Handle cases where the fp16 data is stored in the
    # non-raw data field
    if logits_weight.raw_data:
        if pad_along_axis_1:
            padding_data = np.zeros((logits_weight.dims[0], padding), dtype=np.float16)
            weight_with_padding = np.concatenate((NumpyHelper.to_array(logits_weight), padding_data), axis=1)
            logits_weight.dims[1] = padded_vocab_size
        else:
            padding_data = np.zeros((padding, logits_weight.dims[1]), dtype=np.float16)
            weight_with_padding = np.concatenate((NumpyHelper.to_array(logits_weight), padding_data), axis=0)
            logits_weight.dims[0] = padded_vocab_size

        logits_weight.raw_data = weight_with_padding.tobytes()
    else:
        return False

    # Save the model
    OnnxModel.save(decoder_model_proto, onnx_path, save_as_external_data=use_external_data_format)
    return True

