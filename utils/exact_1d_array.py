
def exact_1d_array(x, message):
    """
    Preprocess a 1-dimensional array.

    Parameters
    ----------
    x : array_like
        Array to be preprocessed.
    message : str
        Error message if `x` cannot be interpreter as a 1-dimensional array.

    Returns
    -------
    `numpy.ndarray`
        Preprocessed array.
    """
    x = np.atleast_1d(np.squeeze(x)).astype(float)
    if x.ndim != 1:
        raise ValueError(message)
    return x

