
def test_Poly_exquo_ground():
    assert Poly(2*x + 4).exquo_ground(2) == Poly(x + 2)
    raises(ExactQuotientFailed, lambda: Poly(2*x + 3).exquo_ground(2))

