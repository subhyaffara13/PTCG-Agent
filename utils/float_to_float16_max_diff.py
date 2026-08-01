
def float_to_float16_max_diff(tensor, min_positive_val=5.96e-08, max_finite_val=65504.0):
    """Measure the maximum absolute difference after converting a float tensor to float16."""
    if not isinstance(tensor, TensorProto):
        raise ValueError(f"Expected input type is an ONNX TensorProto but got {type(tensor)}")
    if tensor.data_type != TensorProto.FLOAT:
        raise ValueError("Expected tensor data type is float.")

    float32_data = None
    if tensor.float_data:
        float32_data = np.array(tensor.float_data)

    if tensor.raw_data:
        float32_data = np.frombuffer(tensor.raw_data, dtype="float32")

    if float32_data is None:
        raise RuntimeError("external data not loaded!")

    float16_data = convert_np_to_float16(float32_data, min_positive_val, max_finite_val)
    return np.amax(np.abs(float32_data - np.float32(float16_data)))

