
def num_obs_y(Y):
    """
    Return the number of original observations that correspond to a
    condensed distance matrix.

    Parameters
    ----------
    Y : array_like
        Condensed distance matrix.

    Returns
    -------
    n : int
        The number of observations in the condensed distance matrix `Y`.

    Examples
    --------
    Find the number of original observations corresponding to a
    condensed distance matrix Y.

    >>> from scipy.spatial.distance import num_obs_y
    >>> Y = [1, 2, 3.5, 7, 10, 4]
    >>> num_obs_y(Y)
    4
    """
    Y = _asarray(Y)
    is_valid_y(Y, throw=True, name='Y')
    k = Y.shape[0]
    if k == 0:
        raise ValueError("The number of observations cannot be determined on "
                         "an empty distance matrix.")
    d = int(np.ceil(np.sqrt(k * 2)))
    if (d * (d - 1) / 2) != k:
        raise ValueError("Invalid condensed distance matrix passed. Must be "
                         "some k where k=(n choose 2) for some n >= 2.")
    return d

