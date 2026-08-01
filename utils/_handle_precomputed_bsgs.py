
def _handle_precomputed_bsgs(base, strong_gens, transversals=None,
                             basic_orbits=None, strong_gens_distr=None):
    """
    Calculate BSGS-related structures from those present.

    Explanation
    ===========

    The base and strong generating set must be provided; if any of the
    transversals, basic orbits or distributed strong generators are not
    provided, they will be calculated from the base and strong generating set.

    Parameters
    ==========

    base : the base
    strong_gens : the strong generators
    transversals : basic transversals
    basic_orbits : basic orbits
    strong_gens_distr : strong generators distributed by membership in basic stabilizers

    Returns
    =======

    (transversals, basic_orbits, strong_gens_distr)
        where *transversals* are the basic transversals, *basic_orbits* are the
        basic orbits, and *strong_gens_distr* are the strong generators distributed
        by membership in basic stabilizers.

    Examples
    ========

    >>> from sympy.combinatorics.named_groups import DihedralGroup
    >>> from sympy.combinatorics.util import _handle_precomputed_bsgs
    >>> D = DihedralGroup(3)
    >>> D.schreier_sims()
    >>> _handle_precomputed_bsgs(D.base, D.strong_gens,
    ... basic_orbits=D.basic_orbits)
    ([{0: (2), 1: (0 1 2), 2: (0 2)}, {1: (2), 2: (1 2)}], [[0, 1, 2], [1, 2]], [[(0 1 2), (0 2), (1 2)], [(1 2)]])

    See Also
    ========

    _orbits_transversals_from_bsgs, _distribute_gens_by_base

    """
    if strong_gens_distr is None:
        strong_gens_distr = _distribute_gens_by_base(base, strong_gens)
    if transversals is None:
        if basic_orbits is None:
            basic_orbits, transversals = \
                _orbits_transversals_from_bsgs(base, strong_gens_distr)
        else:
            transversals = \
                _orbits_transversals_from_bsgs(base, strong_gens_distr,
                                           transversals_only=True)
    else:
        if basic_orbits is None:
            base_len = len(base)
            basic_orbits = [None]*base_len
            for i in range(base_len):
                basic_orbits[i] = list(transversals[i].keys())
    return transversals, basic_orbits, strong_gens_distr

