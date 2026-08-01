
def test_prudnikov_1():
    # A. P. Prudnikov, Yu. A. Brychkov and O. I. Marichev (1990).
    # Integrals and Series: More Special Functions, Vol. 3,.
    # Gordon and Breach Science Publisher

    # 7.3.1
    assert can_do([a, -a], [S.Half])
    assert can_do([a, 1 - a], [S.Half])
    assert can_do([a, 1 - a], [Rational(3, 2)])
    assert can_do([a, 2 - a], [S.Half])
    assert can_do([a, 2 - a], [Rational(3, 2)])
    assert can_do([a, 2 - a], [Rational(3, 2)])
    assert can_do([a, a + S.Half], [2*a - 1])
    assert can_do([a, a + S.Half], [2*a])
    assert can_do([a, a + S.Half], [2*a + 1])
    assert can_do([a, a + S.Half], [S.Half])
    assert can_do([a, a + S.Half], [Rational(3, 2)])
    assert can_do([a, a/2 + 1], [a/2])
    assert can_do([1, b], [2])
    assert can_do([1, b], [b + 1], numerical=False)  # Lerch Phi
             # NOTE: branches are complicated for |z| > 1

    assert can_do([a], [2*a])
    assert can_do([a], [2*a + 1])
    assert can_do([a], [2*a - 1])

