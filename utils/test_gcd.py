
def test_gcd():
    f, g = x**3 - 1, x**2 - 1
    s, t = x**2 + x + 1, x + 1
    h, r = x - 1, x**4 + x**3 - x - 1

    F, G, S, T, H, R = [ Poly(u) for u in (f, g, s, t, h, r) ]

    assert F.cofactors(G) == (H, S, T)
    assert F.gcd(G) == H
    assert F.lcm(G) == R

    assert cofactors(f, g) == (h, s, t)
    assert gcd(f, g) == h
    assert lcm(f, g) == r

    assert cofactors(f, g, x) == (h, s, t)
    assert gcd(f, g, x) == h
    assert lcm(f, g, x) == r

    assert cofactors(f, g, (x,)) == (h, s, t)
    assert gcd(f, g, (x,)) == h
    assert lcm(f, g, (x,)) == r

    assert cofactors(F, G) == (H, S, T)
    assert gcd(F, G) == H
    assert lcm(F, G) == R

    assert cofactors(f, g, polys=True) == (H, S, T)
    assert gcd(f, g, polys=True) == H
    assert lcm(f, g, polys=True) == R

    assert cofactors(F, G, polys=False) == (h, s, t)
    assert gcd(F, G, polys=False) == h
    assert lcm(F, G, polys=False) == r

    f, g = 1.0*x**2 - 1.0, 1.0*x - 1.0
    h, s, t = g, 1.0*x + 1.0, 1.0

    assert cofactors(f, g) == (h, s, t)
    assert gcd(f, g) == h
    assert lcm(f, g) == f

    f, g = 1.0*x**2 - 1.0, 1.0*x - 1.0
    h, s, t = g, 1.0*x + 1.0, 1.0

    assert cofactors(f, g) == (h, s, t)
    assert gcd(f, g) == h
    assert lcm(f, g) == f

    assert cofactors(8, 6) == (2, 4, 3)
    assert gcd(8, 6) == 2
    assert lcm(8, 6) == 24

    f, g = x**2 - 3*x - 4, x**3 - 4*x**2 + x - 4
    l = x**4 - 3*x**3 - 3*x**2 - 3*x - 4
    h, s, t = x - 4, x + 1, x**2 + 1

    assert cofactors(f, g, modulus=11) == (h, s, t)
    assert gcd(f, g, modulus=11) == h
    assert lcm(f, g, modulus=11) == l

    f, g = x**2 + 8*x + 7, x**3 + 7*x**2 + x + 7
    l = x**4 + 8*x**3 + 8*x**2 + 8*x + 7
    h, s, t = x + 7, x + 1, x**2 + 1

    assert cofactors(f, g, modulus=11, symmetric=False) == (h, s, t)
    assert gcd(f, g, modulus=11, symmetric=False) == h
    assert lcm(f, g, modulus=11, symmetric=False) == l

    a, b = sqrt(2), -sqrt(2)
    assert gcd(a, b) == gcd(b, a) == sqrt(2)

    a, b = sqrt(-2), -sqrt(-2)
    assert gcd(a, b) == gcd(b, a) == sqrt(2)

    assert gcd(Poly(x - 2, x), Poly(I*x, x)) == Poly(1, x, domain=ZZ_I)

    raises(TypeError, lambda: gcd(x))
    raises(TypeError, lambda: lcm(x))

    f = Poly(-1, x)
    g = Poly(1, x)
    assert lcm(f, g) == Poly(1, x)

    f = Poly(0, x)
    g = Poly([1, 1], x)
    for i in (f, g):
        assert lcm(i, 0) == 0
        assert lcm(0, i) == 0
        assert lcm(i, f) == 0
        assert lcm(f, i) == 0

    f = 4*x**2 + x + 2
    pfz = Poly(f, domain=ZZ)
    pfq = Poly(f, domain=QQ)

    assert pfz.gcd(pfz) == pfz
    assert pfz.lcm(pfz) == pfz
    assert pfq.gcd(pfq) == pfq.monic()
    assert pfq.lcm(pfq) == pfq.monic()
    assert gcd(f, f) == f
    assert lcm(f, f) == f
    assert gcd(f, f, domain=QQ) == monic(f)
    assert lcm(f, f, domain=QQ) == monic(f)

