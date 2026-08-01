
def _fillna_prep(
    values, mask: npt.NDArray[np.bool_] | None = None
) -> npt.NDArray[np.bool_]:
    # boilerplate for _pad_1d, _backfill_1d, _pad_2d, _backfill_2d

    if mask is None:
        mask = isna(values)

    return mask

