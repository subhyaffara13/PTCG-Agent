
def stirling(n, k, d=None, kind=2, signed=False):
    r"""Return Stirling number $S(n, k)$ of the first or second (default) kind.

    The sum of all Stirling numbers of the second kind for $k = 1$
    through $n$ is ``bell(n)``. The recurrence relationship for these numbers
    is:

    .. math :: {0 \brace 0} = 1; {n \brace 0} = {0 \brace k} = 0;

    .. math :: {{n+1} \brace k} = j {n \brace k} + {n \brace {k-1}}

    where $j$ is:
        $n$ for Stirling numbers of the first kind,
        $-n$ for signed Stirling numbers of the first kind,
        $k$ for Stirling numbers of the second kind.

    The first kind of Stirling number counts the number of permutations of
    ``n`` distinct items that have ``k`` cycles; the second kind counts the
    ways in which ``n`` distinct items can be partitioned into ``k`` parts.
    If ``d`` is given, the "reduced Stirling number of the second kind" is
    returned: $S^{d}(n, k) = S(n - d + 1, k - d + 1)$ with $n \ge k \ge d$.
    (This counts the ways to partition $n$ consecutive integers into $k$
    groups with no pairwise difference less than $d$. See example below.)

    To obtain the signed Stirling numbers of the first kind, use keyword
    ``signed=True``. Using this keyword automatically sets ``kind`` to 1.

    Examples
    ========

    >>> from sympy.functions.combinatorial.numbers import stirling, bell
    >>> from sympy.combinatorics import Permutation
    >>> from sympy.utilities.iterables import multiset_partitions, permutations

    First kind (unsigned by default):

    >>> [stirling(6, i, kind=1) for i in range(7)]
    [0, 120, 274, 225, 85, 15, 1]
    >>> perms = list(permutations(range(4)))
    >>> [sum(Permutation(p).cycles == i for p in perms) for i in range(5)]
    [0, 6, 11, 6, 1]
    >>> [stirling(4, i, kind=1) for i in range(5)]
    [0, 6, 11, 6, 1]

    First kind (signed):

    >>> [stirling(4, i, signed=True) for i in range(5)]
    [0, -6, 11, -6, 1]

    Second kind:

    >>> [stirling(10, i) for i in range(12)]
    [0, 1, 511, 9330, 34105, 42525, 22827, 5880, 750, 45, 1, 0]
    >>> sum(_) == bell(10)
    True
    >>> len(list(multiset_partitions(range(4), 2))) == stirling(4, 2)
    True

    Reduced second kind:

    >>> from sympy import subsets, oo
    >>> def delta(p):
    ...    if len(p) == 1:
    ...        return oo
    ...    return min(abs(i[0] - i[1]) for i in subsets(p, 2))
    >>> parts = multiset_partitions(range(5), 3)
    >>> d = 2
    >>> sum(1 for p in parts if all(delta(i) >= d for i in p))
    7
    >>> stirling(5, 3, 2)
    7

    See Also
    ========
    sympy.utilities.iterables.multiset_partitions


    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Stirling_numbers_of_the_first_kind
    .. [2] https://en.wikipedia.org/wiki/Stirling_numbers_of_the_second_kind

    """
    # TODO: make this a class like bell()

    n = as_int(n)
    k = as_int(k)
    if n < 0:
        raise ValueError('n must be nonnegative')
    if k > n:
        return S.Zero
    if d:
        # assert k >= d
        # kind is ignored -- only kind=2 is supported
        return _eval_stirling2(n - d + 1, k - d + 1)
    elif signed:
        # kind is ignored -- only kind=1 is supported
        return S.NegativeOne**(n - k)*_eval_stirling1(n, k)

    if kind == 1:
        return _eval_stirling1(n, k)
    elif kind == 2:
        return _eval_stirling2(n, k)
    else:
        raise ValueError('kind must be 1 or 2, not %s' % k)

