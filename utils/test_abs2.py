
def test_abs2():
    a = Symbol("a", real=False)
    b = Symbol("b", real=False)
    assert abs(a) != a
    assert abs(-a) != a
    assert abs(a + I*b) != sqrt(a**2 + b**2)

