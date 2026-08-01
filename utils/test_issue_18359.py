
def test_issue_18359():
    c1 = Piecewise((0, x < 0), (Min(1, x)/2 - Min(2, x)/2 + Min(3, x)/2, True))
    c2 = Piecewise((Piecewise((0, x < 0), (Min(1, x)/2 - Min(2, x)/2 + Min(3, x)/2, True)), x >= 0), (0, True))
    correct_result = Interval(1, 2)
    result1 = solveset(c1 - Rational(1, 2), x, Interval(0, 3))
    result2 = solveset(c2 - Rational(1, 2), x, Interval(0, 3))
    assert result1 == correct_result
    assert result2 == correct_result

