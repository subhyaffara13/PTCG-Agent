
def test_dummy_order_ambiguous():
    aa, bb = symbols('a b', above_fermi=True)
    i, j, k, l, m = symbols('i j k l m', below_fermi=True, cls=Dummy)
    a, b, c, d, e = symbols('a b c d e', above_fermi=True, cls=Dummy)
    p, q = symbols('p q', cls=Dummy)
    p1, p2, p3, p4 = symbols('p1 p2 p3 p4', above_fermi=True, cls=Dummy)
    p5, p6, p7, p8 = symbols('p5 p6 p7 p8', above_fermi=True, cls=Dummy)
    h1, h2, h3, h4 = symbols('h1 h2 h3 h4', below_fermi=True, cls=Dummy)
    h5, h6, h7, h8 = symbols('h5 h6 h7 h8', below_fermi=True, cls=Dummy)

    A = Function('A')
    B = Function('B')

    from sympy.utilities.iterables import variations

    # A*A*A*A*B  --  ordering of p5 and p4 is used to figure out the rest
    template = A(p1, p2)*A(p4, p1)*A(p2, p3)*A(p3, p5)*B(p5, p4)
    permutator = variations([a, b, c, d, e], 5)
    base = template.subs(zip([p1, p2, p3, p4, p5], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4, p5], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)

    # A*A*A*A*A  --  an arbitrary index is assigned and the rest are figured out
    template = A(p1, p2)*A(p4, p1)*A(p2, p3)*A(p3, p5)*A(p5, p4)
    permutator = variations([a, b, c, d, e], 5)
    base = template.subs(zip([p1, p2, p3, p4, p5], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4, p5], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)

    # A*A*A  --  ordering of p5 and p4 is used to figure out the rest
    template = A(p1, p2, p4, p1)*A(p2, p3, p3, p5)*A(p5, p4)
    permutator = variations([a, b, c, d, e], 5)
    base = template.subs(zip([p1, p2, p3, p4, p5], next(permutator)))
    for permut in permutator:
        subslist = zip([p1, p2, p3, p4, p5], permut)
        expr = template.subs(subslist)
        assert substitute_dummies(expr) == substitute_dummies(base)

