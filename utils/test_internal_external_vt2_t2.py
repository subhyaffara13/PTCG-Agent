
def test_internal_external_VT2T2():
    ii, jj = symbols('i j', below_fermi=True)
    aa, bb = symbols('a b', above_fermi=True)
    k, l = symbols('k l', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)

    v = Function('v')
    t = Function('t')
    dums = _get_ordered_dummies

    exprs = [
        v(k, l, c, d)*t(aa, c, ii, k)*t(bb, d, jj, l),
        v(l, k, c, d)*t(aa, c, ii, l)*t(bb, d, jj, k),
        v(k, l, d, c)*t(aa, d, ii, k)*t(bb, c, jj, l),
        v(l, k, d, c)*t(aa, d, ii, l)*t(bb, c, jj, k),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)
    exprs = [
        v(k, l, c, d)*t(aa, c, ii, k)*t(d, bb, jj, l),
        v(l, k, c, d)*t(aa, c, ii, l)*t(d, bb, jj, k),
        v(k, l, d, c)*t(aa, d, ii, k)*t(c, bb, jj, l),
        v(l, k, d, c)*t(aa, d, ii, l)*t(c, bb, jj, k),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)
    exprs = [
        v(k, l, c, d)*t(c, aa, ii, k)*t(bb, d, jj, l),
        v(l, k, c, d)*t(c, aa, ii, l)*t(bb, d, jj, k),
        v(k, l, d, c)*t(d, aa, ii, k)*t(bb, c, jj, l),
        v(l, k, d, c)*t(d, aa, ii, l)*t(bb, c, jj, k),
    ]
    for permut in exprs[1:]:
        assert dums(exprs[0]) != dums(permut)
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

