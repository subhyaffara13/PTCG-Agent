
def modified_coset_enumeration_r(fp_grp, Y, max_cosets=None, draft=None,
                                    incomplete=False):
    r"""
    Introduce a new set of symbols y \in Y that correspond to the
    generators of the subgroup. Store the elements of Y as a
    word P[\alpha, x] and compute the coset table similar to that of
    the regular coset enumeration methods.

    Examples
    ========

    >>> from sympy.combinatorics.free_groups import free_group
    >>> from sympy.combinatorics.fp_groups import FpGroup
    >>> from sympy.combinatorics.coset_table import modified_coset_enumeration_r
    >>> F, x, y = free_group("x, y")
    >>> f = FpGroup(F, [x**3, y**3, x**-1*y**-1*x*y])
    >>> C = modified_coset_enumeration_r(f, [x])
    >>> C.table
    [[0, 0, 1, 2], [1, 1, 2, 0], [2, 2, 0, 1], [None, 1, None, None], [1, 3, None, None]]

    See Also
    ========

    coset_enumertation_r

    References
    ==========

    .. [1] Holt, D., Eick, B., O'Brien, E.,
           "Handbook of Computational Group Theory",
           Section 5.3.2
    """
    return coset_enumeration_r(fp_grp, Y, max_cosets=max_cosets, draft=draft,
                             incomplete=incomplete, modified=True)

