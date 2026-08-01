
def test_Limits_simple_3a():
    a = Symbol('a')
    #issue 3513
    assert together(limit((x**2 - (a + 1)*x + a)/(x**3 - a**3), x, a)) == \
        (a - 1)/(3*a**2)  # 196

