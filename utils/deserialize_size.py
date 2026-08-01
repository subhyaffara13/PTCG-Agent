
def deserialize_size(sizes: Sequence[SymInt]) -> tuple[int, ...]:
    for sym_int_size in sizes:
        if sym_int_size.type != "as_int":
            raise AssertionError(f"Only as_int is supported, got {sym_int_size.type}")
    return tuple(sym_int_size.as_int for sym_int_size in sizes)

