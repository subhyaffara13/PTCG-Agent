
def _convert_range_to_int(range: ValueRanges):
    if not isinstance(range, ValueRanges):
        raise AssertionError(f"expected ValueRanges, got {type(range)}")
    min_val = _convert_to_int(range.lower)
    max_val = _convert_to_int(range.upper)
    return min_val, max_val

