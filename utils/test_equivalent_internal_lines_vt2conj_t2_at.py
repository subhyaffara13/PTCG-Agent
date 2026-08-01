
def test_equivalent_internal_lines_VT2conjT2_AT():
    # this diagram requires special handling in TCE
    i, j, k, l, m, n = symbols('i j k l m n', below_fermi=True, cls=Dummy)
    a, b, c, d, e, f = symbols('a b c d e f', above_fermi=True, cls=Dummy)
    p1, p2, p3, p4 = symbols('p1 p2 p3 p4', above_fermi=True, cls=Dummy)
    h1, h2, h3, h4 = symbols('h1 h2 h3 h4', below_fermi=True, cls=Dummy)

    from sympy.utilities.iterables import variations

    # atv(abcd)att(abij)att(ijcd)
    template = atv(p1, p2, p3, p4)*att(p1, p2, i, j)*att(i, j, p3, p4)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)
    template = atv(p1, p2, p3, p4)*att(p1, p2, j, i)*att(j, i, p3, p4)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)

    # atv(abcd)att(abij)att(jicd)
    template = atv(p1, p2, p3, p4)*att(p1, p2, i, j)*att(j, i, p3, p4)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)
    template = atv(p1, p2, p3, p4)*att(p1, p2, j, i)*att(i, j, p3, p4)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)

