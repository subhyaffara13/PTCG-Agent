
def np_find_common_type(*dtypes: np.dtype) -> np.dtype:
    """
    np.find_common_type implementation pre-1.25 deprecation using np.result_type
    https://github.com/pandas-dev/pandas/pull/49569#issuecomment-1308300065

    Parameters
    ----------
    dtypes : np.dtypes

    Returns
    -------
    np.dtype
    """
    try:
        common_dtype = np.result_type(*dtypes)
        if common_dtype.kind in "mMSU":
            # NumPy promotion currently (1.25) misbehaves for for times and strings,
            # so fall back to object (find_common_dtype did unless there
            # was only one dtype)
            common_dtype = np.dtype("O")

    except TypeError:
        common_dtype = np.dtype("O")
    return common_dtype

