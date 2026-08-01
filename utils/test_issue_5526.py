
def test_issue_5526():
    assert reduce_inequalities(0 <=
        x + Integral(y**2, (y, 1, 3)) - 1, [x]) == \
        (x >= -Integral(y**2, (y, 1, 3)) + 1)
    f = Function('f')
    e = Sum(f(x), (x, 1, 3))
    assert reduce_inequalities(0 <= x + e + y**2, [x]) == \
        (x >= -y**2 - Sum(f(x), (x, 1, 3)))

