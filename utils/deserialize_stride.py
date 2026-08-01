
def deserialize_stride(strides: Sequence[SymInt]) -> tuple[int, ...]:
    for sym_int_stride in strides:
        if sym_int_stride.type != "as_int":
            raise AssertionError(f"Only as_int is supported, got {sym_int_stride.type}")
    return tuple(sym_int_stride.as_int for sym_int_stride in strides)

