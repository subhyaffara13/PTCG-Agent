
def test_reduced():
    f = 2*x**4 + y**2 - x**2 + y**3
    G = [x**3 - x, y**3 - y]

    Q = [2*x, 1]
    r = x**2 + y**2 + y

    assert reduced(f, G) == (Q, r)
    assert reduced(f, G, x, y) == (Q, r)

    H = groebner(G)

    assert H.reduce(f) == (Q, r)

    Q = [Poly(2*x, x, y), Poly(1, x, y)]
    r = Poly(x**2 + y**2 + y, x, y)

    assert _strict_eq(reduced(f, G, polys=True), (Q, r))
    assert _strict_eq(reduced(f, G, x, y, polys=True), (Q, r))

    H = groebner(G, polys=True)

    assert _strict_eq(H.reduce(f), (Q, r))

    f = 2*x**3 + y**3 + 3*y
    G = groebner([x**2 + y**2 - 1, x*y - 2])

    Q = [x**2 - x*y**3/2 + x*y/2 + y**6/4 - y**4/2 + y**2/4, -y**5/4 + y**3/2 + y*Rational(3, 4)]
    r = 0

    assert reduced(f, G) == (Q, r)
    assert G.reduce(f) == (Q, r)

    assert reduced(f, G, auto=False)[1] != 0
    assert G.reduce(f, auto=False)[1] != 0

    assert G.contains(f) is True
    assert G.contains(f + 1) is False

    assert reduced(1, [1], x) == ([1], 0)
    raises(ComputationFailed, lambda: reduced(1, [1]))

    f_poly = Poly(2*x**3 + y**3 + 3*y)
    G_poly = groebner([Poly(x**2 + y**2 - 1), Poly(x*y - 2)])

    Q_poly = [Poly(x**2 - 1/2*x*y**3 + 1/2*x*y + 1/4*y**6 - 1/2*y**4 + 1/4*y**2, x, y, domain='QQ'),
              Poly(-1/4*y**5 + 1/2*y**3 + 3/4*y, x, y, domain='QQ')]
    r_poly = Poly(0, x, y, domain='QQ')

    assert G_poly.reduce(f_poly) == (Q_poly, r_poly)

    Q, r = G_poly.reduce(f)
    assert all(isinstance(q, Poly) for q in Q)
    assert isinstance(r, Poly)

    f_wrong_gens = Poly(2*x**3 + y**3 + 3*y, x, y, z)
    raises(ValueError, lambda: G_poly.reduce(f_wrong_gens))

    zero_poly = Poly(0, x, y)
    Q, r = G_poly.reduce(zero_poly)
    assert all(q.is_zero for q in Q)
    assert r.is_zero

    const_poly = Poly(1, x, y)
    Q, r = G_poly.reduce(const_poly)
    assert isinstance(r, Poly)
    assert r.as_expr() == 1
    assert all(q.is_zero for q in Q)

