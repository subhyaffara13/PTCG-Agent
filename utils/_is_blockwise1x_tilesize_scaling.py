
def _is_blockwise1xTILESIZE_scaling(
    sz: Any, tensor_sz: Any, tile_size: int, transpose: bool
) -> bool:
    lhs = 1 if transpose else 0
    rhs = 0 if transpose else 1
    return V.graph.sizevars.statically_known_equals(
        sz[lhs], tensor_sz[lhs]
    ) and V.graph.sizevars.statically_known_equals(
        sz[rhs], ceildiv(tensor_sz[rhs], tile_size)
    )

