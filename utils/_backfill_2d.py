
def _backfill_2d(
    values,
    limit: int | None = None,
    limit_area: Literal["inside", "outside"] | None = None,
    mask: npt.NDArray[np.bool_] | None = None,
):
    mask = _fillna_prep(values, mask)
    if limit_area is not None:
        _fill_limit_area_2d(mask, limit_area)

    if values.size:
        algos.backfill_2d_inplace(values, mask, limit=limit)
    else:
        # for test coverage
        pass
    return values, mask

