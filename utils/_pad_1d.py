
def _pad_1d(
    values: np.ndarray,
    limit: int | None = None,
    limit_area: Literal["inside", "outside"] | None = None,
    mask: npt.NDArray[np.bool_] | None = None,
) -> tuple[np.ndarray, npt.NDArray[np.bool_]]:
    mask = _fillna_prep(values, mask)
    if limit_area is not None and not mask.all():
        _fill_limit_area_1d(mask, limit_area)
    algos.pad_inplace(values, mask, limit=limit)
    return values, mask

