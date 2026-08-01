
def exact_2d_array(x, message):
    """
    Preprocess a 2-dimensional array.

    Parameters
    ----------
    x : array_like
        Array to be preprocessed.
    message : str
        Error message if `x` cannot be interpreter as a 2-dimensional array.

    Returns
    -------
    `numpy.ndarray`
        Preprocessed array.
    """
    x = np.atleast_2d(x).astype(float)
    if x.ndim != 2:
        raise ValueError(message)
    return x

