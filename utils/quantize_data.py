
def quantize_data(
    data, qType, symmetric, reduce_range=False, min_real_range=None, rmin_override=None, rmax_override=None
) -> tuple[numpy.ndarray, numpy.ndarray, numpy.ndarray]:
    """
    :param data: data to quantize
    :param qType: data type to quantize to.
    :param symmetric: whether symmetric quantization is used or not.
    :parameter reduce_range: True if the quantization range should be reduced. Defaults to False.
    :parameter min_real_range: Minimum floating-point range (i.e., rmax - rmin) to enforce. Defaults to None.
    :parameter rmin_override: The value of rmin to use if not None. Otherwise, uses min(data).
    :parameter rmax_override: The value of rmax to use if not None. Otherwise, uses max(data).
    :return: minimum, maximum, zero point, scale, and quantized weights

    To pack weights, we compute a linear transformation

    - when data `type == uint8` mode, from `[rmin, rmax]` -> :math:`[0, 2^{b-1}]` and
    - when data `type == int8`, from `[-m , m]` -> :math:`[-(2^{b-1}-1), 2^{b-1}-1]` where
        `m = max(abs(rmin), abs(rmax))`

    and add necessary intermediate nodes to transform quantized weight to full weight using the equation

    :math:`r = S(q-z)`, where

    - *r*: real original value
    - *q*: quantized value
    - *S*: scale
    - *z*: zero point
    """
    zero_point, scale = compute_data_quant_params(
        data,
        qType,
        symmetric,
        reduce_range,
        min_real_range,
        rmin_override,
        rmax_override,
    )
    if qType == TensorProto.FLOAT8E4M3FN:
        quantized_data = quantize_nparray(qType, data, scale, zero_point)
        if any((quantized_data.view(numpy.uint8).ravel() & 127) == 127):
            np_data = numpy.asarray(data)
            raise RuntimeError(
                f"One of the quantized value is NaN data in [{np_data.min()}, {np_data.max()}], "
                f"quantized_data in [{quantized_data.min()}, {quantized_data.max()}]."
            )
        return zero_point, scale, quantized_data

    if qType in (
        TensorProto.INT8,
        TensorProto.UINT8,
        TensorProto.INT16,
        TensorProto.UINT16,
        TensorProto.INT4,
        TensorProto.UINT4,
    ):
        quantized_data = quantize_nparray(qType, data, scale, zero_point)
        return zero_point, scale, quantized_data

    raise ValueError(f"Unexpected value for qType={qType}.")

