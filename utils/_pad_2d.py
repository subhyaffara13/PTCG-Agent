
def _pad_2d(
    values: np.ndarray,
    limit: int | None = None,
    limit_area: Literal["inside", "outside"] | None = None,
    mask: npt.NDArray[np.bool_] | None = None,
) -> tuple[np.ndarray, npt.NDArray[np.bool_]]:
    mask = _fillna_prep(values, mask)
    if limit_area is not None:
        _fill_limit_area_2d(mask, limit_area)

    if values.size:
        algos.pad_2d_inplace(values, mask, limit=limit)
    return values, mask

