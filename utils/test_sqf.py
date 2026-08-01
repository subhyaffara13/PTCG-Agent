
def test_sqf():
    f = x**5 - x**3 - x**2 + 1
    g = x**3 + 2*x**2 + 2*x + 1
    h = x - 1

    p = x**4 + x**3 - x - 1

    F, G, H, P = map(Poly, (f, g, h, p))

    assert F.sqf_part() == P
    assert sqf_part(f) == p
    assert sqf_part(f, x) == p
    assert sqf_part(f, (x,)) == p
    assert sqf_part(F) == P
    assert sqf_part(f, polys=True) == P
    assert sqf_part(F, polys=False) == p

    assert F.sqf_list() == (1, [(G, 1), (H, 2)])
    assert sqf_list(f) == (1, [(g, 1), (h, 2)])
    assert sqf_list(f, x) == (1, [(g, 1), (h, 2)])
    assert sqf_list(f, (x,)) == (1, [(g, 1), (h, 2)])
    assert sqf_list(F) == (1, [(G, 1), (H, 2)])
    assert sqf_list(f, polys=True) == (1, [(G, 1), (H, 2)])
    assert sqf_list(F, polys=False) == (1, [(g, 1), (h, 2)])

    assert F.sqf_list_include() == [(G, 1), (H, 2)]

    raises(ComputationFailed, lambda: sqf_part(4))

    assert sqf(1) == 1
    assert sqf_list(1) == (1, [])

    assert sqf((2*x**2 + 2)**7) == 128*(x**2 + 1)**7

    assert sqf(f) == g*h**2
    assert sqf(f, x) == g*h**2
    assert sqf(f, (x,)) == g*h**2

    d = x**2 + y**2

    assert sqf(f/d) == (g*h**2)/d
    assert sqf(f/d, x) == (g*h**2)/d
    assert sqf(f/d, (x,)) == (g*h**2)/d

    assert sqf(x - 1) == x - 1
    assert sqf(-x - 1) == -x - 1

    assert sqf(x - 1) == x - 1
    assert sqf(6*x - 10) == Mul(2, 3*x - 5, evaluate=False)

    assert sqf((6*x - 10)/(3*x - 6)) == Rational(2, 3)*((3*x - 5)/(x - 2))
    assert sqf(Poly(x**2 - 2*x + 1)) == (x - 1)**2

    f = 3 + x - x*(1 + x) + x**2

    assert sqf(f) == 3

    f = (x**2 + 2*x + 1)**20000000000

    assert sqf(f) == (x + 1)**40000000000
    assert sqf_list(f) == (1, [(x + 1, 40000000000)])

    # https://github.com/sympy/sympy/issues/26497
    assert sqf(expand(((y - 2)**2 * (y + 2) * (x + 1)))) == \
        (y - 2)**2 * expand((y + 2) * (x + 1))
    assert sqf(expand(((y - 2)**2 * (y + 2) * (z + 1)))) == \
        (y - 2)**2 * expand((y + 2) * (z + 1))
    assert sqf(expand(((y - I)**2 * (y + I) * (x + 1)))) == \
        (y - I)**2 * expand((y + I) * (x + 1))
    assert sqf(expand(((y - I)**2 * (y + I) * (z + 1)))) == \
        (y - I)**2 * expand((y + I) * (z + 1))

    # Check that factors are combined and sorted.
    p = (x - 2)**2*(x - 1)*(x + y)**2*(y - 2)**2*(y - 1)
    assert Poly(p).sqf_list() == (1, [
        (Poly(x*y - x - y + 1), 1),
        (Poly(x**2*y - 2*x**2 + x*y**2 - 4*x*y + 4*x - 2*y**2 + 4*y), 2)
    ])

