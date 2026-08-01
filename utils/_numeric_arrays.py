
def _numeric_arrays(arrays, kinds='buifc', xp=None):
    """
    See if a list of arrays are all numeric.

    Parameters
    ----------
    arrays : array or list of arrays
        arrays to check if numeric.
    kinds : string-like
        The dtypes of the arrays to be checked. If the dtype.kind of
        the ndarrays are not in this string the function returns False and
        otherwise returns True.
    """
    if xp is None:
        xp = array_namespace(*arrays)
    if not is_numpy(xp):
        return True

    if type(arrays) is np.ndarray:
        return arrays.dtype.kind in kinds
    for array_ in arrays:
        if array_.dtype.kind not in kinds:
            return False
    return True

