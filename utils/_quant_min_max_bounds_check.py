
def _quant_min_max_bounds_check(quant_min, quant_max, dtype):
    if dtype not in _DTYPE_TO_QVALUE_BOUNDS:
        raise ValueError(f"Unsupported dtype: {dtype}")
    quant_min_lower_bound, quant_max_upper_bound = _DTYPE_TO_QVALUE_BOUNDS[dtype]

    if quant_min < quant_min_lower_bound:
        raise AssertionError(
            "quant_min out of bound for dtype, "
            f"quant_min_lower_bound: {quant_min_lower_bound} quant_min: {quant_min}"
        )

    if quant_max > quant_max_upper_bound:
        raise AssertionError(
            "quant_max out of bound for dtype, "
            f"quant_max_upper_bound: {quant_max_upper_bound} quant_max: {quant_max}"
        )

