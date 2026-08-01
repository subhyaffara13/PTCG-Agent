
def first_in_class(C, Y=()):
    """
    Checks whether the subgroup ``H=G1`` corresponding to the Coset Table
    could possibly be the canonical representative of its conjugacy class.

    Parameters
    ==========

    C: CosetTable

    Returns
    =======

    bool: True/False

    If this returns False, then no descendant of C can have that property, and
    so we can abandon C. If it returns True, then we need to process further
    the node of the search tree corresponding to C, and so we call
    ``descendant_subgroups`` recursively on C.

    Examples
    ========

    >>> from sympy.combinatorics import free_group
    >>> from sympy.combinatorics.fp_groups import FpGroup, CosetTable, first_in_class
    >>> F, x, y = free_group("x, y")
    >>> f = FpGroup(F, [x**2, y**3, (x*y)**4])
    >>> C = CosetTable(f, [])
    >>> C.table = [[0, 0, None, None]]
    >>> first_in_class(C)
    True
    >>> C.table = [[1, 1, 1, None], [0, 0, None, 1]]; C.p = [0, 1]
    >>> first_in_class(C)
    True
    >>> C.table = [[1, 1, 2, 1], [0, 0, 0, None], [None, None, None, 0]]
    >>> C.p = [0, 1, 2]
    >>> first_in_class(C)
    False
    >>> C.table = [[1, 1, 1, 2], [0, 0, 2, 0], [2, None, 0, 1]]
    >>> first_in_class(C)
    False

    # TODO:: Sims points out in [Sim94] that performance can be improved by
    # remembering some of the information computed by ``first_in_class``. If
    # the ``continue alpha`` statement is executed at line 14, then the same thing
    # will happen for that value of alpha in any descendant of the table C, and so
    # the values the values of alpha for which this occurs could profitably be
    # stored and passed through to the descendants of C. Of course this would
    # make the code more complicated.

    # The code below is taken directly from the function on page 208 of [Sim94]
    # nu[alpha]

    """
    n = C.n
    # lamda is the largest numbered point in Omega_c_alpha which is currently defined
    lamda = -1
    # for alpha in Omega_c, nu[alpha] is the point in Omega_c_alpha corresponding to alpha
    nu = [None]*n
    # for alpha in Omega_c_alpha, mu[alpha] is the point in Omega_c corresponding to alpha
    mu = [None]*n
    # mutually nu and mu are the mutually-inverse equivalence maps between
    # Omega_c_alpha and Omega_c
    next_alpha = False
    # For each 0!=alpha in [0 .. nc-1], we start by constructing the equivalent
    # standardized coset table C_alpha corresponding to H_alpha
    for alpha in range(1, n):
        # reset nu to "None" after previous value of alpha
        for beta in range(lamda+1):
            nu[mu[beta]] = None
        # we only want to reject our current table in favour of a preceding
        # table in the ordering in which 1 is replaced by alpha, if the subgroup
        # G_alpha corresponding to this preceding table definitely contains the
        # given subgroup
        for w in Y:
            # TODO: this should support input of a list of general words
            # not just the words which are in "A" (i.e gen and gen^-1)
            if C.table[alpha][C.A_dict[w]] != alpha:
                # continue with alpha
                next_alpha = True
                break
        if next_alpha:
            next_alpha = False
            continue
        # try alpha as the new point 0 in Omega_C_alpha
        mu[0] = alpha
        nu[alpha] = 0
        # compare corresponding entries in C and C_alpha
        lamda = 0
        for beta in range(n):
            for x in C.A:
                gamma = C.table[beta][C.A_dict[x]]
                delta = C.table[mu[beta]][C.A_dict[x]]
                # if either of the entries is undefined,
                # we move with next alpha
                if gamma is None or delta is None:
                    # continue with alpha
                    next_alpha = True
                    break
                if nu[delta] is None:
                    # delta becomes the next point in Omega_C_alpha
                    lamda += 1
                    nu[delta] = lamda
                    mu[lamda] = delta
                if nu[delta] < gamma:
                    return False
                if nu[delta] > gamma:
                    # continue with alpha
                    next_alpha = True
                    break
            if next_alpha:
                next_alpha = False
                break
    return True

