
def maybe_infer_ndim(values, placement: BlockPlacement, ndim: int | None) -> int:
    """
    If `ndim` is not provided, infer it from placement and values.
    """
    warnings.warn(
        "maybe_infer_ndim is deprecated and will be removed in a future version.",
        Pandas4Warning,
        stacklevel=2,
    )
    return _maybe_infer_ndim(values, placement, ndim)

