
def _is_blockwise128x128_scaling(sz: Any, tensor_sz: Any) -> bool:
    return V.graph.sizevars.statically_known_equals(
        sz[0], ceildiv(tensor_sz[0], 128)
    ) and V.graph.sizevars.statically_known_equals(sz[1], ceildiv(tensor_sz[1], 128))

