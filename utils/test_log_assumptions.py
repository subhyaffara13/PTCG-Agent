
def test_log_assumptions():
    p = symbols('p', positive=True)
    n = symbols('n', negative=True)
    z = symbols('z', zero=True)
    x = symbols('x', infinite=True, extended_positive=True)

    assert log(z).is_positive is False
    assert log(x).is_extended_positive is True
    assert log(2) > 0
    assert log(1, evaluate=False).is_zero
    assert log(1 + z).is_zero
    assert log(p).is_zero is None
    assert log(n).is_zero is False
    assert log(0.5).is_negative is True
    assert log(exp(p) + 1).is_positive

    assert log(1, evaluate=False).is_algebraic
    assert log(42, evaluate=False).is_algebraic is False

    assert log(1 + z).is_rational

