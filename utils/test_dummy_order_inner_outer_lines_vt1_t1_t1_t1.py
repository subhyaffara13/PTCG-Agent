
def test_dummy_order_inner_outer_lines_VT1T1T1T1():
    ii, jj = symbols('i j', below_fermi=True)
    aa, bb = symbols('a b', above_fermi=True)
    k, l = symbols('k l', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)

    v = Function('v')
    t = Function('t')
    dums = _get_ordered_dummies

    # Coupled-Cluster T2 terms with V*T1*T1*T1*T1
    exprs = [
        # permut t <=> swapping external lines, not equivalent
        # except if v has certain symmetries.
        v(k, l, c, d)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
        v(k, l, c, d)*t(c, jj)*t(d, ii)*t(aa, k)*t(bb, l),
        v(k, l, c, d)*t(c, ii)*t(d, jj)*t(bb, k)*t(aa, l),
        v(k, l, c, d)*t(c, jj)*t(d, ii)*t(bb, k)*t(aa, l),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)
    exprs = [
        # permut v <=> swapping external lines, not equivalent
        # except if v has certain symmetries.
        #
        # Note that in contrast to above, these permutations have identical
        # dummy order.  That is because the proximity to external indices
        # has higher influence on the canonical dummy ordering than the
        # position of a dummy on the factors.  In fact, the terms here are
        # similar in structure as the result of the dummy substitutions above.
        v(k, l, c, d)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
        v(l, k, c, d)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
        v(k, l, d, c)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
        v(l, k, d, c)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) == dums(permut)
        assert substitute_dummies(exprs[0]) != substitute_dummies(permut)
    exprs = [
        # permut t and v <=> swapping internal lines, equivalent.
        # Canonical dummy order is different, and a consistent
        # substitution reveals the equivalence.
        v(k, l, c, d)*t(c, ii)*t(d, jj)*t(aa, k)*t(bb, l),
        v(k, l, d, c)*t(c, jj)*t(d, ii)*t(aa, k)*t(bb, l),
        v(l, k, c, d)*t(c, ii)*t(d, jj)*t(bb, k)*t(aa, l),
        v(l, k, d, c)*t(c, jj)*t(d, ii)*t(bb, k)*t(aa, l),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

