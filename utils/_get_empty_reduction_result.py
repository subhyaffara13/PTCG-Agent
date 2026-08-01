
def _get_empty_reduction_result(
    shape: Shape,
    axis: AxisInt,
) -> np.ndarray:
    """
    The result from a reduction on an empty ndarray.

    Parameters
    ----------
    shape : Tuple[int, ...]
    axis : int

    Returns
    -------
    np.ndarray
    """
    shp = np.array(shape)
    dims = np.arange(len(shape))
    ret = np.empty(shp[dims != axis], dtype=np.float64)
    ret.fill(np.nan)
    return ret

