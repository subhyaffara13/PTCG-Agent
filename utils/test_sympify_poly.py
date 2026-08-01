
def test_sympify_poly():
    p = Poly(x**2 + x + 1, x)

    assert _sympify(p) is p
    assert sympify(p) is p

