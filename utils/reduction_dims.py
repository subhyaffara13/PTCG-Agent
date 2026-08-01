
def reduction_dims(shape: ShapeType, dims: Sequence | None) -> tuple[int, ...]:
    if dims is None:
        return tuple(range(len(shape)))
    dims = tuple(canonicalize_dim(len(shape), idx) for idx in dims)
    validate_no_repeating_dims(dims)
    return dims

