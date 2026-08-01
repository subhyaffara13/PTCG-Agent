
def test_issue_3204():
    x = Symbol("x", nonnegative=True)
    f = sin(x**3)**Rational(1, 3)
    assert f.nseries(x, 0, 17) == x - x**7/18 - x**13/3240 + O(x**17)

