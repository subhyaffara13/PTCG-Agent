
def test_issue_14831():
    a = -2*sqrt(2)*sqrt(12*sqrt(2) + 17)
    assert minimal_polynomial(a, x) == x**2 + 16*x - 8
    e = (-3*sqrt(12*sqrt(2) + 17) + 12*sqrt(2) +
         17 - 2*sqrt(2)*sqrt(12*sqrt(2) + 17))
    assert minimal_polynomial(e, x) == x

