
def test_CRootOf_eval_rational():
    p = legendre_poly(4, x, polys=True)
    roots = [r.eval_rational(n=18) for r in p.real_roots()]
    for root in roots:
        assert isinstance(root, Rational)
    roots = [str(root.n(17)) for root in roots]
    assert roots == [
            "-0.86113631159405258",
            "-0.33998104358485626",
             "0.33998104358485626",
             "0.86113631159405258",
             ]

