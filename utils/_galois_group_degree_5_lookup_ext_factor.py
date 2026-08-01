
def _galois_group_degree_5_lookup_ext_factor(T, max_tries=30, randomize=False):
    r"""
    Compute the Galois group of a polynomial of degree 5.

    Explanation
    ===========

    Based on Alg 6.3.9 of [1], but uses resolvent coeff lookup, plus
    factorization over an algebraic extension.

    """
    from sympy.combinatorics.galois import S5TransitiveSubgroups

    _T = T

    history = set()
    for i in range(max_tries):
        R_dup = get_resolvent_by_lookup(T, 1)
        if dup_sqf_p(R_dup, ZZ):
            break
        _, T = tschirnhausen_transformation(T, max_tries=max_tries,
                                            history=history,
                                            fixed_order=not randomize)
    else:
        raise MaxTriesException

    sq_disc = has_square_disc(T)

    if dup_irreducible_p(R_dup, ZZ):
        return ((S5TransitiveSubgroups.A5, True) if sq_disc
                else (S5TransitiveSubgroups.S5, False))

    if not sq_disc:
        return (S5TransitiveSubgroups.M20, False)

    # If we get this far, Gal(T) can only be D5 or C5.
    # But for Gal(T) to have order 5, T must already split completely in
    # the extension field obtained by adjoining a single one of its roots.
    fl = Poly(_T, domain=ZZ.alg_field_from_poly(_T)).factor_list()[1]
    if len(fl) == 5:
        return (S5TransitiveSubgroups.C5, True)
    else:
        return (S5TransitiveSubgroups.D5, True)

