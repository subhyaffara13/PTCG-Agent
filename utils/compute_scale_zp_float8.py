
def compute_scale_zp_float8(element_type, std):
    """Calculate the scale s for a float8 type (E4M3FN).
    The function assumes the coefficient distribution and the float 8
    distribution are similar to two gaussian laws.

    :return: zero and scale [z, s]

    More details in notebook `quantization_fp8.ipynb
    <https://github.com/microsoft/onnxruntime/blob/main/docs/python/notebooks/quantization_fp8.ipynb>`_.
    """
    zp_dtype = None
    if element_type not in FLOAT8_DISTRIBUTIONS:
        if element_type == TensorProto.FLOAT8E4M3FN:
            from ml_dtypes import float8_e4m3fn  # noqa: PLC0415

            zp_dtype = float8_e4m3fn
            all_values = [float(i) for i in range(256)]
            values = numpy.array(
                [f for f in all_values if not numpy.isnan(f) and not numpy.isinf(f)], dtype=numpy.float32
            )
        else:
            raise ValueError(f"Quantization to element_type={element_type} not implemented.")
        FLOAT8_DISTRIBUTIONS[element_type] = values
    elif element_type == TensorProto.FLOAT8E4M3FN:
        from ml_dtypes import float8_e4m3fn  # noqa: PLC0415

        zp_dtype = float8_e4m3fn

    if zp_dtype is None:
        raise TypeError(f"Unexpected element_type {element_type}.")
    std_f8 = numpy.std(FLOAT8_DISTRIBUTIONS[element_type])
    zero = numpy.array(0, dtype=zp_dtype)
    scale = numpy.array(std / std_f8, dtype=std.dtype)
    return [zero, scale]

