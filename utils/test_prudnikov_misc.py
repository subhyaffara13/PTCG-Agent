
def test_prudnikov_misc():
    assert can_do([1, (3 + I)/2, (3 - I)/2], [Rational(3, 2), 2])
    assert can_do([S.Half, a - 1], [Rational(3, 2), a + 1], lowerplane=True)
    assert can_do([], [b + 1])
    assert can_do([a], [a - 1, b + 1])

    assert can_do([a], [a - S.Half, 2*a])
    assert can_do([a], [a - S.Half, 2*a + 1])
    assert can_do([a], [a - S.Half, 2*a - 1])
    assert can_do([a], [a + S.Half, 2*a])
    assert can_do([a], [a + S.Half, 2*a + 1])
    assert can_do([a], [a + S.Half, 2*a - 1])
    assert can_do([S.Half], [b, 2 - b])
    assert can_do([S.Half], [b, 3 - b])
    assert can_do([1], [2, b])

    assert can_do([a, a + S.Half], [2*a, b, 2*a - b + 1])
    assert can_do([a, a + S.Half], [S.Half, 2*a, 2*a + S.Half])
    assert can_do([a], [a + 1], lowerplane=True)  # lowergamma

