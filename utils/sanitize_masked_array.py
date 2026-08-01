
def sanitize_masked_array(data: ma.MaskedArray) -> np.ndarray:
    """
    Convert numpy MaskedArray to ensure mask is softened.
    """
    mask = ma.getmaskarray(data)
    if mask.any():
        dtype, fill_value = maybe_promote(data.dtype, np.nan)
        dtype = cast(np.dtype, dtype)
        data = ma.asarray(data.astype(dtype, copy=True))
        data.soften_mask()  # set hardmask False if it was True
        data[mask] = fill_value
    else:
        data = data.copy()
    return data

