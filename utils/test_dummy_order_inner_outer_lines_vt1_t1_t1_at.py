
def test_dummy_order_inner_outer_lines_VT1T1T1_AT():
    ii = symbols('i', below_fermi=True)
    aa = symbols('a', above_fermi=True)
    k, l = symbols('k l', below_fermi=True, cls=Dummy)
    c, d = symbols('c d', above_fermi=True, cls=Dummy)

    # Coupled-Cluster T1 terms with V*T1*T1*T1
    # t^{a}_{k} t^{c}_{i} t^{d}_{l} v^{lk}_{dc}
    exprs = [
        # permut v and t <=> swapping internal lines, equivalent
        # irrespective of symmetries in v
        atv(k, l, c, d)*att(c, ii)*att(d, l)*att(aa, k),
        atv(l, k, c, d)*att(c, ii)*att(d, k)*att(aa, l),
        atv(k, l, d, c)*att(d, ii)*att(c, l)*att(aa, k),
        atv(l, k, d, c)*att(d, ii)*att(c, k)*att(aa, l),
    ]
    for permut in exprs[1:]:
        assert substitute_dummies(exprs[0]) == substitute_dummies(permut)

