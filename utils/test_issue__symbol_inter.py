
def test_issue_Symbol_inter():
    i = Interval(0, oo)
    r = S.Reals
    mat = Matrix([0, 0, 0])
    assert Intersection(r, i, FiniteSet(m), FiniteSet(m, n)) == \
        Intersection(i, FiniteSet(m))
    assert Intersection(FiniteSet(1, m, n), FiniteSet(m, n, 2), i) == \
        Intersection(i, FiniteSet(m, n))
    assert Intersection(FiniteSet(m, n, x), FiniteSet(m, z), r) == \
        Intersection(Intersection({m, z}, {m, n, x}), r)
    assert Intersection(FiniteSet(m, n, 3), FiniteSet(m, n, x), r) == \
        Intersection(FiniteSet(3, m, n), FiniteSet(m, n, x), r, evaluate=False)
    assert Intersection(FiniteSet(m, n, 3), FiniteSet(m, n, 2, 3), r) == \
        Intersection(FiniteSet(3, m, n), r)
    assert Intersection(r, FiniteSet(mat, 2, n), FiniteSet(0, mat, n)) == \
        Intersection(r, FiniteSet(n))
    assert Intersection(FiniteSet(sin(x), cos(x)), FiniteSet(sin(x), cos(x), 1), r) == \
        Intersection(r, FiniteSet(sin(x), cos(x)))
    assert Intersection(FiniteSet(x**2, 1, sin(x)), FiniteSet(x**2, 2, sin(x)), r) == \
        Intersection(r, FiniteSet(x**2, sin(x)))

