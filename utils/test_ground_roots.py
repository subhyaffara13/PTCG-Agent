
def test_ground_roots():
    f = x**6 - 4*x**4 + 4*x**3 - x**2

    assert Poly(f).ground_roots() == {S.One: 2, S.Zero: 2}
    assert ground_roots(f) == {S.One: 2, S.Zero: 2}

