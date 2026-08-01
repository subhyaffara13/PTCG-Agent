
def _nanargminmax(values: np.ndarray, mask: npt.NDArray[np.bool_], func) -> int:
    """
    See nanargminmax.__doc__.
    """
    idx = np.arange(values.shape[0])
    non_nans = values[~mask]
    non_nan_idx = idx[~mask]

    return non_nan_idx[func(non_nans)]

