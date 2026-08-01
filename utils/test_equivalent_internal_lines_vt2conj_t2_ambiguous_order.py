
def test_equivalent_internal_lines_VT2conjT2_ambiguous_order():
    # These diagrams invokes _determine_ambiguous() because the
    # dummies can not be ordered unambiguously by the key alone
    i, j, k, l, m, n = symbols('i j k l m n', below_fermi=True, cls=Dummy)
    a, b, c, d, e, f = symbols('a b c d e f', above_fermi=True, cls=Dummy)
    p1, p2, p3, p4 = symbols('p1 p2 p3 p4', above_fermi=True, cls=Dummy)
    h1, h2, h3, h4 = symbols('h1 h2 h3 h4', below_fermi=True, cls=Dummy)

    from sympy.utilities.iterables import variations

    v = Function('v')
    t = Function('t')
    dums = _get_ordered_dummies

    # v(abcd)t(abij)t(cdij)
    template = v(p1, p2, p3, p4)*t(p1, p2, i, j)*t(p3, p4, i, j)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert dums(base) != dums(expr)
        assert substitute_dummies(expr) == substitute_dummies(base)
    template = v(p1, p2, p3, p4)*t(p1, p2, j, i)*t(p3, p4, i, j)
    permutator = variations([a, b, c, d], 4)
    base = template.subs(zip([p1, p2, p3, p4], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4], permut)
        expr = template.subs(subslist)
        assert dums(base) != dums(expr)
        assert substitute_dummies(expr) == substitute_dummies(base)

