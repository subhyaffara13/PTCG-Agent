
def _get_padding_value(dtype, padding_type):
    if dtype.is_floating_point:
        return (
            torch.finfo(dtype).max if padding_type == "max" else torch.finfo(dtype).min
        )
    else:
        # For integer dtypes, use infinity sentinels which the C++ implementation
        # clamps to dtype min/max, avoiding precision loss through double.
        return float("inf") if padding_type == "max" else float("-inf")

