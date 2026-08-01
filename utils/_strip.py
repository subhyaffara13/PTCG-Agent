
def _strip(g, base, orbits, transversals):
    """
    Attempt to decompose a permutation using a (possibly partial) BSGS
    structure.

    Explanation
    ===========

    This is done by treating the sequence ``base`` as an actual base, and
    the orbits ``orbits`` and transversals ``transversals`` as basic orbits and
    transversals relative to it.

    This process is called "sifting". A sift is unsuccessful when a certain
    orbit element is not found or when after the sift the decomposition
    does not end with the identity element.

    The argument ``transversals`` is a list of dictionaries that provides
    transversal elements for the orbits ``orbits``.

    Parameters
    ==========

    g : permutation to be decomposed
    base : sequence of points
    orbits : list
        A list in which the ``i``-th entry is an orbit of ``base[i]``
        under some subgroup of the pointwise stabilizer of `
        `base[0], base[1], ..., base[i - 1]``. The groups themselves are implicit
        in this function since the only information we need is encoded in the orbits
        and transversals
    transversals : list
        A list of orbit transversals associated with the orbits *orbits*.

    Examples
    ========

    >>> from sympy.combinatorics import Permutation, SymmetricGroup
    >>> from sympy.combinatorics.util import _strip
    >>> S = SymmetricGroup(5)
    >>> S.schreier_sims()
    >>> g = Permutation([0, 2, 3, 1, 4])
    >>> _strip(g, S.base, S.basic_orbits, S.basic_transversals)
    ((4), 5)

    Notes
    =====

    The algorithm is described in [1],pp.89-90. The reason for returning
    both the current state of the element being decomposed and the level
    at which the sifting ends is that they provide important information for
    the randomized version of the Schreier-Sims algorithm.

    References
    ==========

    .. [1] Holt, D., Eick, B., O'Brien, E."Handbook of computational group theory"

    See Also
    ========

    sympy.combinatorics.perm_groups.PermutationGroup.schreier_sims
    sympy.combinatorics.perm_groups.PermutationGroup.schreier_sims_random

    """
    h = g._array_form
    base_len = len(base)
    for i in range(base_len):
        beta = h[base[i]]
        if beta == base[i]:
            continue
        if beta not in orbits[i]:
            return _af_new(h), i + 1
        u = transversals[i][beta]._array_form
        h = _af_rmul(_af_invert(u), h)
    return _af_new(h), base_len + 1

