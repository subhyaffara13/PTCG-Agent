
def test_Float_issue_2107():
    a = Float(0.1, 10)
    b = Float("0.1", 10)

    assert a - a == 0
    assert a + (-a) == 0
    assert S.Zero + a - a == 0
    assert S.Zero + a + (-a) == 0

    assert b - b == 0
    assert b + (-b) == 0
    assert S.Zero + b - b == 0
    assert S.Zero + b + (-b) == 0

