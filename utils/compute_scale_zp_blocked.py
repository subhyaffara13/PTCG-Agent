
def compute_scale_zp_blocked(
    weight: numpy.ndarray,
    quant_type: int,
    axis: int,
    block_size: int,
    symmetric: bool,
) -> tuple[numpy.ndarray, numpy.ndarray]:
    """Compute per-block scale and zero-point for a weight tensor.

    The weight is sliced along *axis* into blocks of *block_size* elements.
    Per the ONNX opset-21 spec, QuantizeLinear/DequantizeLinear require the
    scale and zero_point tensors to have the **same rank** as the input tensor.
    Only rank-2 weight tensors are supported; rank > 2 is explicitly rejected.

    Returns arrays with the same rank and dimensions as *weight*, except
    ``shape[axis] == ceil(weight.shape[axis] / block_size)``. This matches
    the ONNX opset-21 QuantizeLinear/DequantizeLinear blocked-quantization spec.

    :param weight: Float32/float16 weight array (must be rank-2).
    :param quant_type: ONNX tensor data type for quantization.
    :param axis: Axis along which to apply block-wise quantization.
    :param block_size: Number of elements per block along *axis*.
    :param symmetric: Whether to use symmetric quantization per block.
    :return: Tuple of (zero_point, scale), each with shape matching *weight*
        except ``shape[axis] == n_blocks``, where ``n_blocks == ceil(weight.shape[axis] / block_size)``.
    :raises NotImplementedError: If weight rank is not 2 (opset-21 constraint).
    """
    if weight.ndim != 2:
        raise NotImplementedError(
            f"Per-block (opset-21) quantization is only supported for rank-2 weight tensors. "
            f"Got rank-{weight.ndim} tensor with shape {weight.shape}. "
            "For rank > 2 tensors, reshape to 2-D before quantizing or use per-channel quantization."
        )

    k = weight.shape[axis]
    n_blocks = (k + block_size - 1) // block_size

    # Flatten all non-axis dims into a single "other" dimension.
    other = int(numpy.prod([d for i, d in enumerate(weight.shape) if i != axis]))
    # Move the quantized axis to position 0 for easy slicing.
    moved = numpy.moveaxis(weight, axis, 0)  # shape: [k, other]
    moved = moved.reshape(k, other)

    qmin, qmax = get_qmin_qmax_for_qType(quant_type, reduce_range=False, symmetric=symmetric)
    zp_dtype = ONNX_INT_TYPE_RANGE[quant_type][0].dtype

    # Pad along axis-0 to a multiple of block_size for vectorised reduction.
    pad_len = n_blocks * block_size - k
    if pad_len > 0:
        pad = numpy.zeros((pad_len, other), dtype=moved.dtype)
        moved_padded = numpy.concatenate([moved, pad], axis=0)
    else:
        moved_padded = moved

    # Reshape to [n_blocks, block_size, other] for axis-based min/max.
    blocks = moved_padded.reshape(n_blocks, block_size, other)

    # Compute per-block min/max vectorised (no Python loop over blocks or cols).
    rmin = blocks.min(axis=1)  # [n_blocks, other]
    rmax = blocks.max(axis=1)  # [n_blocks, other]

    # Clamp to include zero, matching compute_scale_zp semantics.
    rmin = numpy.minimum(rmin, numpy.zeros_like(rmin))
    rmax = numpy.maximum(rmax, numpy.zeros_like(rmax))

    if symmetric:
        absmax = numpy.maximum(numpy.abs(rmin), numpy.abs(rmax))
        rmin = -absmax
        rmax = absmax

    qmin_val = numpy.float64(qmin)
    qmax_val = numpy.float64(qmax)
    dr = (rmax - rmin).astype(numpy.float64)
    dq = qmax_val - qmin_val
    raw_scale = (dr / dq).astype(weight.dtype)

    tiny = numpy.finfo(weight.dtype).tiny
    degenerate = raw_scale < tiny  # blocks where the float range is essentially zero

    scales = numpy.where(degenerate, numpy.ones_like(raw_scale), raw_scale)

    if symmetric:
        zp_val = int(numpy.round((qmin_val + qmax_val) / 2.0))
        zero_points = numpy.full((n_blocks, other), zp_val, dtype=zp_dtype)
    else:
        raw_zp = numpy.round(qmin_val - rmin.astype(numpy.float64) / scales.astype(numpy.float64))
        raw_zp = numpy.clip(raw_zp, qmin_val, qmax_val)
        zero_points = raw_zp.astype(zp_dtype)
        zero_points[degenerate] = 0

    # Move the block axis back to its original position so the returned arrays have
    # the same rank as the weight and shape[axis] == n_blocks, as required by the
    # ONNX opset-21 QuantizeLinear/DequantizeLinear spec.
    scales = numpy.moveaxis(scales, 0, axis)
    zero_points = numpy.moveaxis(zero_points, 0, axis)

    return zero_points, scales

