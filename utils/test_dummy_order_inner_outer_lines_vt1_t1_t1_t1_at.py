
def test_dummy_order_inner_outer_lines_VT1T1T1T1_AT():
    ii, jj = symbols('i j', below_fermi=True)
    aa, bb = symbols('a b', above_fermi=True)
    k, l = symbols('k l', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)

    # Coupled-Cluster T2 terms with V*T1*T1*T1*T1
    # non-equivalent substitutions (change of sign)
    exprs = [
        # permut t <=> swapping external lines
        atv(k, l, c, d)*att(c, ii)*att(d, jj)*att(aa, k)*att(bb, l),
        atv(k, l, c, d)*att(c, jj)*att(d, ii)*att(aa, k)*att(bb, l),
        atv(k, l, c, d)*att(c, ii)*att(d, jj)*att(bb, k)*att(aa, l),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == -substitute_dummies(permut)

    # equivalent substitutions
    exprs = [
        atv(k, l, c, d)*att(c, ii)*att(d, jj)*att(aa, k)*att(bb, l),
        # permut t <=> swapping external lines
        atv(k, l, c, d)*att(c, jj)*att(d, ii)*att(bb, k)*att(aa, l),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

