
def get_qrange_for_qType(qType, reduce_range=False, symmetric=False):  # noqa: N802
    """
    Helper function to get the quantization range for a type.
        parameter qType: quantization type.
        return: quantization range.
    """
    qmin, qmax = get_qmin_qmax_for_qType(qType, reduce_range, symmetric=symmetric)
    return qmax - qmin

