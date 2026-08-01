
def _compute_sizes(seq, scalar_type):
    MAX_DIMS = 128
    is_storage = _isStorage(seq)
    sizes = []
    # TODO: this is inaccurate, we actually test PySequence_Check
    while isinstance(seq, (list, tuple)):
        length = len(seq)
        if is_storage:
            length //= scalar_type.itemsize
        sizes.append(length)
        if len(sizes) > MAX_DIMS:
            raise ValueError(f"too many dimensions '{type(seq).__name__}'")
        if length == 0:
            break
        try:
            handle = seq[0]
        except Exception:
            raise ValueError(  # noqa: B904
                f"could not determine the shape of object type '{type(seq).__name__}'"
            )
        seq = handle

    return sizes

