
def test_issue_3792():
    assert limit((1 - cos(x))/x**2, x, S.Half) == 4 - 4*cos(S.Half)
    assert limit(sin(sin(x + 1) + 1), x, 0) == sin(1 + sin(1))
    assert limit(abs(sin(x + 1) + 1), x, 0) == 1 + sin(1)

