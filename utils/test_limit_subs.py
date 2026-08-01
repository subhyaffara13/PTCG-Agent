
def test_limit_subs():
    for F in (Sum, Product, Integral):
        assert F(a*exp(a), (a, -2, 2)) == F(a*exp(a), (a, -b, b)).subs(b, 2)
        assert F(a, (a, F(b, (b, 1, 2)), 4)).subs(F(b, (b, 1, 2)), c) == \
            F(a, (a, c, 4))
        assert F(x, (x, 1, x + y)).subs(x, 1) == F(x, (x, 1, y + 1))

