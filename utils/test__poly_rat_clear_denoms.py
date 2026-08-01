
def test_Poly_rat_clear_denoms():
    f = Poly(x**2/y + 1, x)
    g = Poly(x**3 + y, x)

    assert f.rat_clear_denoms(g) == \
        (Poly(x**2 + y, x), Poly(y*x**3 + y**2, x))

    f = f.set_domain(EX)
    g = g.set_domain(EX)

    assert f.rat_clear_denoms(g) == (f, g)

