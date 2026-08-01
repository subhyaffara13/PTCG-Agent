
def _holder_formula(prime_factors):
    r""" Number of groups of order `n`.
    where `n` is squarefree and its prime factors are ``prime_factors``.
    i.e., ``n == math.prod(prime_factors)``

    Explanation
    ===========

    When `n` is squarefree, the number of groups of order `n` is expressed by

    .. math ::
        \sum_{d \mid n} \prod_p \frac{p^{c(p, d)} - 1}{p - 1}

    where `n=de`, `p` is the prime factor of `e`,
    and `c(p, d)` is the number of prime factors `q` of `d` such that `q \equiv 1 \pmod{p}` [2]_.

    The formula is elegant, but can be improved when implemented as an algorithm.
    Since `n` is assumed to be squarefree, the divisor `d` of `n` can be identified with the power set of prime factors.
    We let `N` be the set of prime factors of `n`.
    `F = \{p \in N : \forall q \in N, q \not\equiv 1 \pmod{p} \}, M = N \setminus F`, we have the following.

    .. math ::
        \sum_{d \in 2^{M}} \prod_{p \in M \setminus d} \frac{p^{c(p, F \cup d)} - 1}{p - 1}

    Practically, many prime factors are expected to be members of `F`, thus reducing computation time.

    Parameters
    ==========

    prime_factors : set
        The set of prime factors of ``n``. where `n` is squarefree.

    Returns
    =======

    int : Number of groups of order ``n``

    Examples
    ========

    >>> from sympy.combinatorics.group_numbers import _holder_formula
    >>> _holder_formula({2}) # n = 2
    1
    >>> _holder_formula({2, 3}) # n = 2*3 = 6
    2

    See Also
    ========

    groups_count

    References
    ==========

    .. [1] Otto Holder, Die Gruppen der Ordnungen p^3, pq^2, pqr, p^4,
           Math. Ann. 43 pp. 301-412 (1893).
           http://dx.doi.org/10.1007/BF01443651
    .. [2] John H. Conway, Heiko Dietrich and E.A. O'Brien,
           Counting groups: gnus, moas and other exotica
           The Mathematical Intelligencer 30, 6-15 (2008)
           https://doi.org/10.1007/BF02985731

    """
    F = {p for p in prime_factors if all(q % p != 1 for q in prime_factors)}
    M = prime_factors - F

    s = 0
    powerset = chain.from_iterable(combinations(M, r) for r in range(len(M)+1))
    for ps in powerset:
        ps = set(ps)
        prod = 1
        for p in M - ps:
            c = len([q for q in F | ps if q % p == 1])
            prod *= (p**c - 1) // (p - 1)
            if not prod:
                break
        s += prod
    return s

