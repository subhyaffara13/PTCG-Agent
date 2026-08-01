
def _stabilizer(degree, generators, alpha):
    r"""Return the stabilizer subgroup of ``alpha``.

    Explanation
    ===========

    The stabilizer of `\alpha` is the group `G_\alpha =
    \{g \in G | g(\alpha) = \alpha\}`.
    For a proof of correctness, see [1], p.79.

    degree :       degree of G
    generators :   generators of G

    Examples
    ========

    >>> from sympy.combinatorics.perm_groups import _stabilizer
    >>> from sympy.combinatorics.named_groups import DihedralGroup
    >>> G = DihedralGroup(6)
    >>> _stabilizer(G.degree, G.generators, 5)
    [(5)(0 4)(1 3), (5)]

    See Also
    ========

    orbit

    """
    orb = [alpha]
    table = {alpha: list(range(degree))}
    table_inv = {alpha: list(range(degree))}
    used = [False]*degree
    used[alpha] = True
    gens = [x._array_form for x in generators]
    stab_gens = []
    for b in orb:
        for gen in gens:
            temp = gen[b]
            if used[temp] is False:
                gen_temp = _af_rmul(gen, table[b])
                orb.append(temp)
                table[temp] = gen_temp
                table_inv[temp] = _af_invert(gen_temp)
                used[temp] = True
            else:
                schreier_gen = _af_rmuln(table_inv[temp], gen, table[b])
                if schreier_gen not in stab_gens:
                    stab_gens.append(schreier_gen)
    return [_af_new(x) for x in stab_gens]

