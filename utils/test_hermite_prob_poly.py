
def test_hermite_prob_poly():
    raises(ValueError, lambda: hermite_prob_poly(-1, x))

    assert hermite_prob_poly(1, x, polys=True) == Poly(x)

    assert hermite_prob_poly(0, x) == 1
    assert hermite_prob_poly(1, x) == x
    assert hermite_prob_poly(2, x) == x**2 - 1
    assert hermite_prob_poly(3, x) == x**3 - 3*x
    assert hermite_prob_poly(4, x) == x**4 - 6*x**2 + 3
    assert hermite_prob_poly(5, x) == x**5 - 10*x**3 + 15*x
    assert hermite_prob_poly(6, x) == x**6 - 15*x**4 + 45*x**2 - 15

    assert hermite_prob_poly(1).dummy_eq(x)
    assert hermite_prob_poly(1, polys=True) == Poly(x)

