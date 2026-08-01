
def _subarray_str(dtype):
    base, shape = dtype.subdtype
    return f"({_construction_repr(base, short=True)}, {shape})"

