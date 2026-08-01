
def _validate_collapse_args(a: Tensor, start: int, end: int) -> None:
    # Special-case for zero dimensional tensors
    ndim = max(1, a.dim())
    utils.validate_idx(ndim, start)
    utils.validate_idx(ndim, end)

    # Verifies end is strictly greater than start
    # (Collapse requires a non-empty interval)
    torch._check_value(
        end >= start,
        lambda: f"Attempting to collapse but end, {end}, is less than start, {start}!",
    )

