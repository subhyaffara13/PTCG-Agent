
def test_heurisch_fractions():
    assert heurisch(1/x, x) == log(x)
    assert heurisch(1/(2 + x), x) == log(x + 2)
    assert heurisch(1/(x + sin(y)), x) == log(x + sin(y))

    # Up to a constant, where C = pi*I*Rational(5, 12), Mathematica gives identical
    # result in the first case. The difference is because SymPy changes
    # signs of expressions without any care.
    # XXX ^ ^ ^ is this still correct?
    assert heurisch(5*x**5/(
        2*x**6 - 5), x) in [5*log(2*x**6 - 5) / 12, 5*log(-2*x**6 + 5) / 12]
    assert heurisch(5*x**5/(2*x**6 + 5), x) == 5*log(2*x**6 + 5) / 12

    assert heurisch(1/x**2, x) == -1/x
    assert heurisch(-1/x**5, x) == 1/(4*x**4)

