
def _astype_float_to_int_nansafe(
    values: np.ndarray, dtype: np.dtype, copy: bool
) -> np.ndarray:
    """
    astype with a check preventing converting NaN to a meaningless integer value.
    """
    if not np.isfinite(values).all():
        raise IntCastingNaNError(
            "Cannot convert non-finite values (NA or inf) to integer."
            "Replace or remove non-finite values or cast to an integer type"
            "that supports these values (e.g. 'Int64')"
        )
    if dtype.kind == "u":
        # GH#45151
        if not (values >= 0).all():
            raise ValueError(f"Cannot losslessly cast from {values.dtype} to {dtype}")
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=RuntimeWarning)
        return values.astype(dtype, copy=copy)

