
def test_roots_strict():
    assert roots(x**2 - 2*x + 1, strict=False) == {1: 2}
    assert roots(x**2 - 2*x + 1, strict=True) == {1: 2}

    assert roots(x**6 - 2*x**5 - x**2 + 3*x - 2, strict=False) == {2: 1}
    raises(UnsolvableFactorError, lambda: roots(x**6 - 2*x**5 - x**2 + 3*x - 2, strict=True))

