
def unique_roots(p, tol=1e-3, rtype='min'):
    """Determine unique roots and their multiplicities from a list of roots.

    Parameters
    ----------
    p : array_like
        The list of roots.
    tol : float, optional
        The tolerance for two roots to be considered equal in terms of
        the distance between them. Default is 1e-3. Refer to Notes about
        the details on roots grouping.
    rtype : {'max', 'maximum', 'min', 'minimum', 'avg', 'mean'}, optional
        How to determine the returned root if multiple roots are within
        `tol` of each other.

        - 'max', 'maximum': pick the maximum of those roots
        - 'min', 'minimum': pick the minimum of those roots
        - 'avg', 'mean': take the average of those roots

        When finding minimum or maximum among complex roots they are compared
        first by the real part and then by the imaginary part.

    Returns
    -------
    unique : ndarray
        The list of unique roots.
    multiplicity : ndarray
        The multiplicity of each root.

    Notes
    -----
    If we have 3 roots ``a``, ``b`` and ``c``, such that ``a`` is close to
    ``b`` and ``b`` is close to ``c`` (distance is less than `tol`), then it
    doesn't necessarily mean that ``a`` is close to ``c``. It means that roots
    grouping is not unique. In this function we use "greedy" grouping going
    through the roots in the order they are given in the input `p`.

    This utility function is not specific to roots but can be used for any
    sequence of values for which uniqueness and multiplicity has to be
    determined. For a more general routine, see `numpy.unique`.

    Examples
    --------
    >>> from scipy import signal
    >>> vals = [0, 1.3, 1.31, 2.8, 1.25, 2.2, 10.3]
    >>> uniq, mult = signal.unique_roots(vals, tol=2e-2, rtype='avg')

    Check which roots have multiplicity larger than 1:

    >>> uniq[mult > 1]
    array([ 1.305])
    """
    if rtype in ['max', 'maximum']:
        reduce = np.max
    elif rtype in ['min', 'minimum']:
        reduce = np.min
    elif rtype in ['avg', 'mean']:
        reduce = np.mean
    else:
        raise ValueError("`rtype` must be one of "
                         "{'max', 'maximum', 'min', 'minimum', 'avg', 'mean'}")

    p = np.asarray(p)

    points = np.empty((len(p), 2))
    points[:, 0] = np.real(p)
    points[:, 1] = np.imag(p)
    tree = cKDTree(points)

    p_unique = []
    p_multiplicity = []
    used = np.zeros(len(p), dtype=bool)
    for i in range(len(p)):
        if used[i]:
            continue

        group = tree.query_ball_point(points[i], tol)
        group = [x for x in group if not used[x]]

        p_unique.append(reduce(p[group]))
        p_multiplicity.append(len(group))

        used[group] = True

    return np.asarray(p_unique), np.asarray(p_multiplicity)

