
def compute_scale_zp(rmin, rmax, qmin, qmax, symmetric=False, min_real_range=None):
    """Calculate the scale s and zero point z for the quantization relation
    r = s(q-z), where r are the original values and q are the corresponding
    quantized values.

    r and z are calculated such that every value within [rmin,rmax] has an
    approximate representation within [qmin,qmax]. In addition, qmin <= z <=
    qmax is enforced. If the symmetric flag is set to True, the interval
    [rmin,rmax] is symmetrized to [-absmax, +absmax], where
    absmax = max(abs(rmin), abs(rmax)).

    :parameter rmin: minimum value of r
    :parameter rmax: maximum value of r
    :parameter qmin: minimum value representable by the target quantization data type
    :parameter qmax: maximum value representable by the target quantization data type
    :parameter symmetric: True if the floating-point range should be made symmetric. Defaults to False.
    :parameter min_real_range: Minimum floating-point range (i.e., rmax - rmin) to enforce. Defaults to None.
    :return: zero and scale [z, s]

    """
    if qmin > 0 or qmax < 0:
        raise ValueError(f"qmin and qmax must meet requirement: qmin <= 0 <= qmax while qmin:{qmin}, qmmax:{qmax}")

    # Adjust rmin and rmax such that 0 is included in the range. This is
    # required to make sure zero can be represented by the quantization data
    # type (i.e. to make sure qmin <= zero_point <= qmax)
    rmin = numpy.minimum(rmin, numpy.array(0, dtype=rmin.dtype))
    rmax = numpy.maximum(rmax, numpy.array(0, dtype=rmax.dtype))

    # Ensure a minimum float-point range if specified.
    if min_real_range is not None:
        rmax = max(rmax, rmin + numpy.asarray(min_real_range, dtype=rmin.dtype))

    if symmetric:
        absmax = numpy.maximum(numpy.abs(rmin), numpy.abs(rmax))
        rmin = -absmax
        rmax = +absmax

    assert qmin <= qmax, f"qmin={rmin} > qmax={rmax}"
    dr = numpy.array(rmax - rmin, dtype=numpy.float64)
    dq = numpy.array(qmax, dtype=numpy.float64) - numpy.array(qmin, dtype=numpy.float64)
    scale = numpy.array(dr / dq)
    assert scale >= 0, "scale issue"
    if scale < numpy.finfo(rmax.dtype).tiny:
        scale = numpy.array(1.0, dtype=rmax.dtype)
        zero_point = numpy.array(0, dtype=qmin.dtype)
    else:
        if symmetric:
            # When symmetric (i.e., rmax == -rmin), the zero_point formula reduces to round((qmax + qmin) / 2.0).
            # This simpler formula doesn't depend on scale and guarantees that the zero point values
            # for int8, uint8, int16, and uint16 are always 0, 128, 0, and 32768, respectively.
            # This is important for per-channel/symmetric QLinearConv on CPU EP, which requires all channels to have
            # the exact same zero_point values.
            zero_point = numpy.array(
                numpy.round((qmin + qmax) / numpy.array(2.0, dtype=numpy.float64)), dtype=qmin.dtype
            )
        else:
            zero_point = numpy.array(numpy.round(qmin - rmin / scale), dtype=qmin.dtype)
        scale = scale.astype(rmax.dtype)

    return [zero_point, scale]

