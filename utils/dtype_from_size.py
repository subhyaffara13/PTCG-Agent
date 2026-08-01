
def dtype_from_size(size: int) -> torch.dtype:
    from .virtualized import V

    if V.graph.sizevars.statically_known_lt(
        size, 2**31
    ) and V.graph.sizevars.statically_known_geq(size, -(2**31)):
        return torch.int32
    else:
        return torch.int64

