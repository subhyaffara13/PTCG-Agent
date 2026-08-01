
def create_weight_matching(float_model_path: str, qdq_model_path: str) -> dict[str, dict[str, numpy.ndarray]]:
    """Comparing weight values to help debugging accuracy loss due to quantization.

    This functions takes the float model and the qdq model, and provides a data structure for comparing
    their corresponding weights to locate quantization errors

    Arg:
        float_model_path: Path points to the float point model.
        qdq_model_path: Path points to the qdq model.

    Returns:
        Dict for comparing weight tensors. E.g.
        ```
        qdq_weight_cmp = create_weight_matching(float_model, qdq_model)
        print(qdq_weight_cmp['activation1']['float'])
        print(qdq_weight_cmp['activation1']['dequantized'])
        ```
    """
    float_onnx_model = ONNXModel(load_model_with_shape_infer(Path(float_model_path)))
    qdq_onnx_model = ONNXModel(load_model_with_shape_infer(Path(qdq_model_path)))

    matched_weights: dict[str, dict[str, numpy.ndarray]] = {}
    initializers = qdq_onnx_model.initializer()
    for node in qdq_onnx_model.nodes():
        if node.op_type != DEQUANT_OP_NAME:
            continue  # Only care about DQ node
        weight_name: str = node.input[0]
        weight_values = find_by_name(weight_name, initializers)
        if not weight_values:
            continue  # Only care about DQ node with const inputs
        if not weight_name.endswith(TENSOR_NAME_QUANT_SUFFIX):
            logging.error(f"Model Error in '{qdq_model_path}': Dequantized tensor name '{weight_name}' not recognized!")
            continue

        axis = -1
        for attr in node.attribute:
            if attr.name == "axis":
                axis = attr.i

        weight_tensor = numpy_helper.to_array(weight_values)
        weight_scale = numpy_helper.to_array(find_by_name(node.input[1], initializers))
        if len(node.input) > 2:
            weight_zp = numpy_helper.to_array(find_by_name(node.input[2], initializers))
        else:
            weight_zp = numpy.zeros(weight_scale.shape, dtype=numpy.int32)

        # Perform dequantization:
        if weight_scale.size == weight_zp.size == 1:
            # Avoids the confusion between a scaler and a tensor of one element.
            weight_scale = weight_scale.reshape(())
            weight_zp = weight_zp.reshape(())
        if weight_scale.shape != weight_zp.shape:
            raise RuntimeError(
                f"scale and zero_point must have the same shape but {weight_scale.shape} != {weight_zp.shape}"
            )
        weight_quant = _run_dequantize_linear(weight_tensor, weight_scale, weight_zp, channel_axis=axis)
        weight_name = weight_name[: -len(TENSOR_NAME_QUANT_SUFFIX)]
        if weight_quant is None:
            logging.error(f"Model Error in '{qdq_model_path}': '{weight_name}' per-channel quantization on 0 channel")
            continue

        float_values = find_by_name(weight_name, float_onnx_model.initializer())
        if not float_values:
            logging.error(f"Model Error in '{float_model_path}': weight tensor '{weight_name}' not found!")
            continue
        weight_float = numpy_helper.to_array(float_values)
        matched_weights[weight_name] = {"float": weight_float, "dequantized": weight_quant}

    return matched_weights

