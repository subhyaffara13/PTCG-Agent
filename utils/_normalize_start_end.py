
def _normalize_start_end(
    x: Tensor, dim: int, start: int | None, end: int | None
) -> tuple[int, int]:
    """
    Normalize start and end such that both are in the range
    [0, x.get_size()[dim]] and start <= end.
    """
    dim_size = x.shape[dim]

    def clamp_wrap(val, lower, upper, default) -> int:
        if val is None:
            return default
        if val < 0:
            val = val + dim_size
        return min(max(val, lower), upper)

    start = clamp_wrap(start, 0, dim_size, 0)
    end = clamp_wrap(end, start, dim_size, dim_size)
    return start, end

