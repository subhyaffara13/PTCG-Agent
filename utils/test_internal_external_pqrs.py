
def test_internal_external_pqrs():
    ii, jj = symbols('i j')
    aa, bb = symbols('a b')
    k, l = symbols('k l', cls=Dummy)
    c, d = symbols('c d', cls=Dummy)

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

