
def is_valid_dm(D, tol=0.0, throw=False, name="D", warning=False):
    """
    Return True if input array satisfies basic distance matrix properties
    (symmetry and zero diagonal).

    This function checks whether the input is a 2-dimensional square NumPy array
    with a zero diagonal and symmetry within a specified tolerance. These are
    necessary properties for a distance matrix but not sufficient -- in particular,
    this function does **not** check the triangle inequality, which is required
    for a true metric distance matrix.

    The triangle inequality states that for any three points ``i``, ``j``, and ``k``:
    ``D[i,k] <= D[i,j] + D[j,k]``

    Parameters
    ----------
    D : array_like
        The candidate object to test for basic distance matrix properties.
    tol : float, optional
        The distance matrix is considered symmetric if the absolute difference
        between entries ``ij`` and ``ji`` is less than or equal to `tol`. The same
        tolerance is used to determine whether diagonal entries are effectively zero.
    throw : bool, optional
        If True, raises an exception when the input is invalid.
    name : str, optional
        The name of the variable to check. This is used in exception messages when
        `throw` is True to identify the offending variable.
    warning : bool, optional
        If True, a warning message is raised instead of throwing an exception.

    Returns
    -------
    valid : bool
        True if the input satisfies the symmetry and zero-diagonal conditions.

    Raises
    ------
    ValueError
        If `throw` is True and `D` is not a valid distance matrix.
    UserWarning
        If `warning` is True and `D` is not a valid distance matrix.

    Notes
    -----
    This function does not check the triangle inequality, which is required for
    a complete validation of a metric distance matrix. Only structural properties
    (symmetry and zero diagonal) are verified. Small numerical deviations from symmetry
    or exact zero diagonal are tolerated within the `tol` parameter.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.spatial.distance import is_valid_dm

    This matrix is a valid distance matrix.

    >>> d = np.array([[0.0, 1.1, 1.2, 1.3],
    ...               [1.1, 0.0, 1.0, 1.4],
    ...               [1.2, 1.0, 0.0, 1.5],
    ...               [1.3, 1.4, 1.5, 0.0]])
    >>> is_valid_dm(d)
    True

    In the following examples, the input is not a valid distance matrix.

    Not square:

    >>> is_valid_dm([[0, 2, 2], [2, 0, 2]])
    False

    Nonzero diagonal element:

    >>> is_valid_dm([[0, 1, 1], [1, 2, 3], [1, 3, 0]])
    False

    Not symmetric:

    >>> is_valid_dm([[0, 1, 3], [2, 0, 1], [3, 1, 0]])
    False

    """
    D = np.asarray(D, order='c')
    valid = True
    try:
        s = D.shape
        if len(D.shape) != 2:
            if name:
                raise ValueError(f"Distance matrix '{name}' must have shape=2 "
                                 "(i.e. be two-dimensional).")
            else:
                raise ValueError('Distance matrix must have shape=2 (i.e. '
                                 'be two-dimensional).')
        if tol == 0.0:
            if not (D == D.T).all():
                if name:
                    raise ValueError(f"Distance matrix '{name}' must be symmetric.")
                else:
                    raise ValueError('Distance matrix must be symmetric.')
            if not (D[range(0, s[0]), range(0, s[0])] == 0).all():
                if name:
                    raise ValueError(f"Distance matrix '{name}' diagonal must be zero.")
                else:
                    raise ValueError('Distance matrix diagonal must be zero.')
        else:
            if not (D - D.T <= tol).all():
                if name:
                    raise ValueError(f'Distance matrix \'{name}\' must be '
                                     f'symmetric within tolerance {tol:5.5f}.')
                else:
                    raise ValueError('Distance matrix must be symmetric within '
                                     f'tolerance {tol:5.5f}.')
            if not (D[range(0, s[0]), range(0, s[0])] <= tol).all():
                if name:
                    raise ValueError(f'Distance matrix \'{name}\' diagonal must be '
                                     f'close to zero within tolerance {tol:5.5f}.')
                else:
                    raise ValueError(('Distance matrix \'{}\' diagonal must be close '
                                      'to zero within tolerance {:5.5f}.').format(*tol))
    except Exception as e:
        if throw:
            raise
        if warning:
            warnings.warn(str(e), stacklevel=2)
        valid = False
    return valid

