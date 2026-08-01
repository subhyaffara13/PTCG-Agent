
def compute_data_quant_params(
    data: numpy.ndarray,
    quant_type: onnx.TensorProto.DataType,
    symmetric: bool,
    reduce_range: bool = False,
    min_real_range: float | None = None,
    rmin_override: float | None = None,
    rmax_override: float | None = None,
) -> tuple[numpy.ndarray, numpy.ndarray]:
    """
    Returns the zero_point and scale for the given data.

    :param data: The data for which to compute quantization parameters.
    :param quant_type: The quantization data type.
    :param symmetric: whether symmetric quantization is used or not.
    :parameter reduce_range: True if the quantization range should be reduced. Defaults to False.
    :parameter min_real_range: Minimum floating-point range (i.e., rmax - rmin) to enforce. Defaults to None.
    :parameter rmin_override: The value of rmin to use if not None. Otherwise, uses min(data).
    :parameter rmax_override: The value of rmax to use if not None. Otherwise, uses max(data).
    :return: zero point and scale
    """
    if not isinstance(data, numpy.ndarray):
        raise TypeError(f"Weight must be given as an array not {type(data)}.")
    if rmin_override is not None:
        rmin = rmin_override
    else:
        rmin = data.min() if len(data) else 0.0

    if rmax_override is not None:
        rmax = rmax_override
    else:
        rmax = data.max() if len(data) else 0.0

    rmin = numpy.array(rmin, dtype=data.dtype)
    rmax = numpy.array(rmax, dtype=data.dtype)
    scale = numpy.array(1.0, dtype=data.dtype)

    if quant_type == TensorProto.FLOAT8E4M3FN:
        if reduce_range:
            raise RuntimeError("Unsupported option reduce_range=True for float 8.")
        std = numpy.std(data)
        zero_point, scale = compute_scale_zp_float8(quant_type, std)
        return _check_type(zero_point, scale, zero_point_index=0)

    if quant_type in (
        TensorProto.INT8,
        TensorProto.UINT8,
        TensorProto.INT16,
        TensorProto.UINT16,
        TensorProto.INT4,
        TensorProto.UINT4,
    ):
        qmin, qmax = get_qmin_qmax_for_qType(quant_type, reduce_range, symmetric=symmetric)
        if len(data):
            zero_point, scale = compute_scale_zp(rmin, rmax, qmin, qmax, symmetric, min_real_range)
        else:
            zero_point = numpy.array(0, dtype=qmin.dtype)
        return _check_type(zero_point, scale, zero_point_index=0)

    raise ValueError(f"Unexpected value for quant_type={quant_type}.")

