
def test_internal_external_VT2T2_AT():
    ii, jj = symbols('i j', below_fermi=True)
    aa, bb = symbols('a b', above_fermi=True)
    k, l = symbols('k l', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)

    exprs = [
        atv(k, l, c, d)*att(aa, c, ii, k)*att(bb, d, jj, l),
        atv(l, k, c, d)*att(aa, c, ii, l)*att(bb, d, jj, k),
        atv(k, l, d, c)*att(aa, d, ii, k)*att(bb, c, jj, l),
        atv(l, k, d, c)*att(aa, d, ii, l)*att(bb, c, jj, k),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)
    exprs = [
        atv(k, l, c, d)*att(aa, c, ii, k)*att(d, bb, jj, l),
        atv(l, k, c, d)*att(aa, c, ii, l)*att(d, bb, jj, k),
        atv(k, l, d, c)*att(aa, d, ii, k)*att(c, bb, jj, l),
        atv(l, k, d, c)*att(aa, d, ii, l)*att(c, bb, jj, k),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)
    exprs = [
        atv(k, l, c, d)*att(c, aa, ii, k)*att(bb, d, jj, l),
        atv(l, k, c, d)*att(c, aa, ii, l)*att(bb, d, jj, k),
        atv(k, l, d, c)*att(d, aa, ii, k)*att(bb, c, jj, l),
        atv(l, k, d, c)*att(d, aa, ii, l)*att(bb, c, jj, k),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

