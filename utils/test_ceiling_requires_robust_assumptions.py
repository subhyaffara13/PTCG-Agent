
def test_ceiling_requires_robust_assumptions():
    assert limit(ceiling(sin(x)), x, 0, "+") == 1
    assert limit(ceiling(sin(x)), x, 0, "-") == 0
    assert limit(ceiling(cos(x)), x, 0, "+") == 1
    assert limit(ceiling(cos(x)), x, 0, "-") == 1
    assert limit(ceiling(5 + sin(x)), x, 0, "+") == 6
    assert limit(ceiling(5 + sin(x)), x, 0, "-") == 5
    assert limit(ceiling(5 + cos(x)), x, 0, "+") == 6
    assert limit(ceiling(5 + cos(x)), x, 0, "-") == 6

