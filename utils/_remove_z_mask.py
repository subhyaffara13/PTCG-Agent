
def _remove_z_mask(
    z: ArrayLike | np.ma.MaskedArray[Any, Any] | None,
) -> tuple[CoordinateArray, MaskArray | None]:
    # Preserve mask if present.
    z_array = np.ma.asarray(z, dtype=np.float64)  # type: ignore[no-untyped-call]
    z_masked = np.ma.masked_invalid(z_array, copy=False)  # type: ignore[no-untyped-call]

    if np.ma.is_masked(z_masked):
        mask = np.ma.getmask(z_masked)
    else:
        mask = None

    return np.ma.getdata(z_masked), mask  # type: ignore[no-untyped-call]

