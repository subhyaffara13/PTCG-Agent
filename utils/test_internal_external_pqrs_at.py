
def test_internal_external_pqrs_AT():
    ii, jj = symbols('i j')
    aa, bb = symbols('a b')
    k, l = symbols('k l', cls=Dummy)
    c, d = symbols('c d', cls=Dummy)

    exprs = [
        atv(k, l, c, d)*att(aa, c, ii, k)*att(bb, d, jj, l),
        atv(l, k, c, d)*att(aa, c, ii, l)*att(bb, d, jj, k),
        atv(k, l, d, c)*att(aa, d, ii, k)*att(bb, c, jj, l),
        atv(l, k, d, c)*att(aa, d, ii, l)*att(bb, c, jj, k),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

