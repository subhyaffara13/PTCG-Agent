
def test_heurisch_hyperbolic():
    assert heurisch(sinh(x), x) == cosh(x)
    assert heurisch(cosh(x), x) == sinh(x)

    assert heurisch(x*sinh(x), x) == x*cosh(x) - sinh(x)
    assert heurisch(x*cosh(x), x) == x*sinh(x) - cosh(x)

    assert heurisch(
        x*asinh(x/2), x) == x**2*asinh(x/2)/2 + asinh(x/2) - x*sqrt(4 + x**2)/4

