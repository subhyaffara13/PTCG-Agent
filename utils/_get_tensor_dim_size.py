
def _get_tensor_dim_size(x: _C.Value, dim: int) -> int | None:
    sizes = _get_tensor_sizes(x)
    return sizes[dim] if sizes else None

