
def quantize_onnx_initializer(
    weight: onnx.TensorProto,
    quant_type: onnx.TensorProto.DataType,
    zero_point: numpy.ndarray,
    scale: numpy.ndarray,
    axis: int | None = None,
    quant_weight_name: str | None = None,
    block_size: int = 0,
) -> onnx.TensorProto:
    """
    Returns a quantized version of the given ONNX initializer.

    :param weight: The ONNX initializer to quantize.
    :param quant_type: The final quantized data type.
    :param zero_point: The zero-point value to use for quantization.
    :param scale: The scale value to use for quantization.
    :param axis: The quantization axis if quantizing per-channel or per-block. Defaults to None.
    :param quant_weight_name: The name of the quantized initializer.
                              If not specified, the quantized name is generated.
    :param block_size: Block size for opset-21 block-wise quantization. 0 means disabled.
    :return: The quantized ONNX initializer.
    """
    weight_data = tensor_proto_to_array(weight)
    q_weight_data: numpy.ndarray | None = None

    if axis is not None and block_size > 0:  # Per-block quantization
        k = weight_data.shape[axis]
        other = int(numpy.prod([d for i, d in enumerate(weight_data.shape) if i != axis]))
        moved = numpy.moveaxis(weight_data, axis, 0).reshape(k, other)
        # scale/zero_point are in spec shape (shape[axis] == n_blocks); move the block
        # axis to position 0 locally so the loop can index [blk, col] uniformly.
        scale_moved = numpy.moveaxis(scale, axis, 0)
        zp_moved = numpy.moveaxis(zero_point, axis, 0)
        n_blocks = scale_moved.shape[0]
        quant_np_dtype = onnx.helper.tensor_dtype_to_np_dtype(quant_type)
        q_moved = numpy.empty_like(moved, dtype=quant_np_dtype)
        for blk in range(n_blocks):
            start = blk * block_size
            end = min(start + block_size, k)
            for col in range(other):
                q_moved[start:end, col] = quantize_nparray(
                    quant_type, moved[start:end, col].ravel(), scale_moved[blk, col], zp_moved[blk, col]
                )
        q_weight_data = numpy.moveaxis(
            q_moved.reshape([k] + [d for i, d in enumerate(weight_data.shape) if i != axis]), 0, axis
        )
    elif axis is None:  # Per-tensor quantization
        q_weight_data = quantize_nparray(quant_type, weight_data.ravel(), scale, zero_point)
    else:  # Per-channel quantization
        channel_count = weight_data.shape[axis]
        channel_dims = list(weight_data.shape)  # deep copy
        channel_dims[axis] = 1  # only one per channel for reshape
        quantized_channel_data_list = []

        for i in range(channel_count):
            channel_data = weight_data.take(i, axis)
            channel_scale = scale[i]
            channel_zero_point = zero_point[i]
            quantized_channel_data = quantize_nparray(
                quant_type, channel_data.ravel(), channel_scale, channel_zero_point
            )
            quantized_channel_data_list.append(numpy.asarray(quantized_channel_data).reshape(channel_dims))

        q_weight_data = numpy.concatenate(quantized_channel_data_list, axis)

    q_weight_name = quant_weight_name if quant_weight_name else f"{weight.name}{TENSOR_NAME_QUANT_SUFFIX}"

    if quant_type == onnx.TensorProto.FLOAT8E4M3FN:
        q_weight_initializer = onnx.TensorProto()
        q_weight_initializer.data_type = quant_type
        q_weight_initializer.dims.extend(weight.dims)
        q_weight_initializer.name = q_weight_name
        # Do not remove .flatten().copy() numpy is not clear about data persistence.
        q_weight_initializer.raw_data = q_weight_data.flatten().copy().tobytes()
        if to_array_extended is not None:
            # This test should not be needed but it helped catch some issues
            # with data persistence and tobytes.
            check = to_array_extended(q_weight_initializer)
            if check.shape != weight_data.shape or check.tobytes() != q_weight_data.tobytes():
                raise RuntimeError(
                    f"The initializer of shape {weight_data.shape} could not be created, expecting "
                    f"{q_weight_data.tobytes()[:10]}, got {check.tobytes()[:10]} and shape={weight.shape}"
                    f"\nraw={str(q_weight_initializer)[:200]}."
                )
    elif quant_type in (onnx.TensorProto.INT4, onnx.TensorProto.UINT4):
        if q_weight_data.dtype not in (int4, uint4):
            raise RuntimeError(f"Quantized weights for {q_weight_name} must be 8-bit before packing as 4-bit values.")

        # We do not use onnx.helper.pack_float32_to_4bit() due to performance.
        # This can be the difference between a large model taking 30 minutes to quantize vs 5 minutes.
        packed_data = bytes(pack_bytes_to_4bit(q_weight_data.tobytes()))

        # We only use onnx.helper.make_tensor with raw data due to bug: https://github.com/onnx/onnx/pull/6161
        q_weight_initializer = onnx.helper.make_tensor(q_weight_name, quant_type, weight.dims, packed_data, raw=True)
    else:
        quant_np_dtype = onnx.helper.tensor_dtype_to_np_dtype(quant_type)
        q_weight_data = numpy.asarray(q_weight_data, dtype=quant_np_dtype).reshape(weight.dims)
        q_weight_initializer = onnx.numpy_helper.from_array(q_weight_data, q_weight_name)

    return q_weight_initializer

