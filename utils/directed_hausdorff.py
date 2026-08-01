
def directed_hausdorff(u, v, rng=0):
    """
    Compute the directed Hausdorff distance between two 2-D arrays.

    Distances between pairs are calculated using a Euclidean metric.

    Parameters
    ----------
    u : (M,N) array_like
        Input array with M points in N dimensions.
    v : (O,N) array_like
        Input array with O points in N dimensions.
    rng : int or `numpy.random.Generator` or None, optional
        Pseudorandom number generator state. Default is 0 so the
        shuffling of `u` and `v` is reproducible.

        If `rng` is passed by keyword, types other than `numpy.random.Generator` are
        passed to `numpy.random.default_rng` to instantiate a ``Generator``.
        If `rng` is already a ``Generator`` instance, then the provided instance is
        used.

        If this argument is passed by position or `seed` is passed by keyword,
        legacy behavior for the argument `seed` applies:

        - If `seed` is None, a new ``RandomState`` instance is used. The state is
          initialized using data from ``/dev/urandom`` (or the Windows analogue)
          if available or from the system clock otherwise.
        - If `seed` is an int, a new ``RandomState`` instance is used,
          seeded with `seed`.
        - If `seed` is already a ``Generator`` or ``RandomState`` instance, then
          that instance is used.

        .. versionchanged:: 1.15.0
            As part of the `SPEC-007 <https://scientific-python.org/specs/spec-0007/>`_
            transition from use of `numpy.random.RandomState` to
            `numpy.random.Generator`, this keyword was changed from `seed` to `rng`.
            For an interim period, both keywords will continue to work, although only
            one may be specified at a time. After the interim period, function calls
            using the `seed` keyword will emit warnings. The behavior of both `seed`
            and `rng` are outlined above, but only the `rng` keyword should be used in
            new code.

    Returns
    -------
    d : double
        The directed Hausdorff distance between arrays `u` and `v`,

    index_1 : int
        index of point contributing to Hausdorff pair in `u`

    index_2 : int
        index of point contributing to Hausdorff pair in `v`

    Raises
    ------
    ValueError
        An exception is thrown if `u` and `v` do not have
        the same number of columns.

    See Also
    --------
    scipy.spatial.procrustes : Another similarity test for two data sets

    Notes
    -----
    Uses the early break technique and the random sampling approach
    described by [1]_. Although worst-case performance is ``O(m * o)``
    (as with the brute force algorithm), this is unlikely in practice
    as the input data would have to require the algorithm to explore
    every single point interaction, and after the algorithm shuffles
    the input points at that. The best case performance is ``O(m)``,
    which is satisfied by selecting an inner loop distance that is
    less than cmax and leads to an early break as often as possible.
    The authors have formally shown that the average runtime is
    closer to ``O(m)``.

    .. versionadded:: 0.19.0

    References
    ----------
    .. [1] A. A. Taha and A. Hanbury, "An efficient algorithm for
           calculating the exact Hausdorff distance." IEEE Transactions On
           Pattern Analysis And Machine Intelligence, vol. 37, no. 11,
           pp. 2153-63, 2015. :doi:`10.1109/TPAMI.2015.2408351`.

    Examples
    --------
    Find the directed Hausdorff distance between two 2-D arrays of
    coordinates:

    >>> from scipy.spatial.distance import directed_hausdorff
    >>> import numpy as np
    >>> u = np.array([(1.0, 0.0),
    ...               (0.0, 1.0),
    ...               (-1.0, 0.0),
    ...               (0.0, -1.0)])
    >>> v = np.array([(2.0, 0.0),
    ...               (0.0, 2.0),
    ...               (-2.0, 0.0),
    ...               (0.0, -4.0)])

    >>> directed_hausdorff(u, v)[0]
    2.23606797749979
    >>> directed_hausdorff(v, u)[0]
    3.0

    Find the general (symmetric) Hausdorff distance between two 2-D
    arrays of coordinates:

    >>> max(directed_hausdorff(u, v)[0], directed_hausdorff(v, u)[0])
    3.0

    Find the indices of the points that generate the Hausdorff distance
    (the Hausdorff pair):

    >>> directed_hausdorff(v, u)[1:]
    (3, 3)

    """
    u = np.asarray(u, dtype=np.float64, order='c')
    v = np.asarray(v, dtype=np.float64, order='c')
    if u.shape[1] != v.shape[1]:
        raise ValueError('u and v need to have the same '
                         'number of columns')
    result = _hausdorff.directed_hausdorff(u, v, rng)
    return result

