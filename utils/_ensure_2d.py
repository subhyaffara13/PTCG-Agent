
def _ensure_2d(values: np.ndarray) -> np.ndarray:
    """
    Reshape 1D values, raise on anything else other than 2D.
    """
    if values.ndim == 1:
        values = values.reshape((values.shape[0], 1))
    elif values.ndim != 2:
        raise ValueError(f"Must pass 2-d input. shape={values.shape}")
    return values

