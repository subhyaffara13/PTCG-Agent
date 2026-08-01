
def is_monotonic(expression, interval=S.Reals, symbol=None):
    """
    Return whether the function is monotonic in the given interval.

    Parameters
    ==========

    expression : Expr
        The target function which is being checked.
    interval : Set, optional
        The range of values in which we are testing (defaults to set of
        all real numbers).
    symbol : Symbol, optional
        The symbol present in expression which gets varied over the given range.

    Returns
    =======

    Boolean
        True if ``expression`` is monotonic in the given ``interval``,
        False otherwise.

    Raises
    ======

    NotImplementedError
        Monotonicity check has not been implemented for the queried function.

    Examples
    ========

    >>> from sympy import is_monotonic
    >>> from sympy.abc import x, y
    >>> from sympy import S, Interval, oo
    >>> is_monotonic(1/(x**2 - 3*x), Interval.open(S(3)/2, 3))
    True
    >>> is_monotonic(1/(x**2 - 3*x), Interval.open(1.5, 3))
    True
    >>> is_monotonic(1/(x**2 - 3*x), Interval.Lopen(3, oo))
    True
    >>> is_monotonic(x**3 - 3*x**2 + 4*x, S.Reals)
    True
    >>> is_monotonic(-x**2, S.Reals)
    False
    >>> is_monotonic(x**2 + y + 1, Interval(1, 2), x)
    True

    """
    from sympy.solvers.solveset import solveset

    expression = sympify(expression)

    free = expression.free_symbols
    if symbol is None and len(free) > 1:
        raise NotImplementedError(
            'is_monotonic has not yet been implemented'
            ' for all multivariate expressions.'
        )

    variable = symbol or (free.pop() if free else Symbol('x'))
    turning_points = solveset(expression.diff(variable), variable, interval)
    return interval.intersection(turning_points) is S.EmptySet


def is_monotonic(Z):
    """
    Return True if the linkage passed is monotonic.

    The linkage is monotonic if for every cluster :math:`s` and :math:`t`
    joined, the distance between them is no less than the distance
    between any previously joined clusters.

    Parameters
    ----------
    Z : ndarray
        The linkage matrix to check for monotonicity.

    Returns
    -------
    b : bool
        A boolean indicating whether the linkage is monotonic.

    See Also
    --------
    linkage : for a description of what a linkage matrix is.

    Examples
    --------
    >>> from scipy.cluster.hierarchy import median, ward, is_monotonic
    >>> from scipy.spatial.distance import pdist

    By definition, some hierarchical clustering algorithms - such as
    `scipy.cluster.hierarchy.ward` - produce monotonic assignments of
    samples to clusters; however, this is not always true for other
    hierarchical methods - e.g. `scipy.cluster.hierarchy.median`.

    Given a linkage matrix ``Z`` (as the result of a hierarchical clustering
    method) we can test programmatically whether it has the monotonicity
    property or not, using `scipy.cluster.hierarchy.is_monotonic`:

    >>> X = [[0, 0], [0, 1], [1, 0],
    ...      [0, 4], [0, 3], [1, 4],
    ...      [4, 0], [3, 0], [4, 1],
    ...      [4, 4], [3, 4], [4, 3]]

    >>> Z = ward(pdist(X))
    >>> Z
    array([[ 0.        ,  1.        ,  1.        ,  2.        ],
           [ 3.        ,  4.        ,  1.        ,  2.        ],
           [ 6.        ,  7.        ,  1.        ,  2.        ],
           [ 9.        , 10.        ,  1.        ,  2.        ],
           [ 2.        , 12.        ,  1.29099445,  3.        ],
           [ 5.        , 13.        ,  1.29099445,  3.        ],
           [ 8.        , 14.        ,  1.29099445,  3.        ],
           [11.        , 15.        ,  1.29099445,  3.        ],
           [16.        , 17.        ,  5.77350269,  6.        ],
           [18.        , 19.        ,  5.77350269,  6.        ],
           [20.        , 21.        ,  8.16496581, 12.        ]])
    >>> is_monotonic(Z)
    True

    >>> Z = median(pdist(X))
    >>> Z
    array([[ 0.        ,  1.        ,  1.        ,  2.        ],
           [ 3.        ,  4.        ,  1.        ,  2.        ],
           [ 9.        , 10.        ,  1.        ,  2.        ],
           [ 6.        ,  7.        ,  1.        ,  2.        ],
           [ 2.        , 12.        ,  1.11803399,  3.        ],
           [ 5.        , 13.        ,  1.11803399,  3.        ],
           [ 8.        , 15.        ,  1.11803399,  3.        ],
           [11.        , 14.        ,  1.11803399,  3.        ],
           [18.        , 19.        ,  3.        ,  6.        ],
           [16.        , 17.        ,  3.5       ,  6.        ],
           [20.        , 21.        ,  3.25      , 12.        ]])
    >>> is_monotonic(Z)
    False

    Note that this method is equivalent to just verifying that the distances
    in the third column of the linkage matrix appear in a monotonically
    increasing order.

    """
    xp = array_namespace(Z)
    Z = _asarray(Z, xp=xp)
    _is_valid_linkage(Z, throw=True, name='Z', xp=xp)

    # We expect the i'th value to be greater than its successor.
    return xp.all(Z[1:, 2] >= Z[:-1, 2])

