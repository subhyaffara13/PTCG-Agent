
def test_exponentiation_of_0():
    x = Symbol('x')
    assert 0**-x == zoo**x
    assert unchanged(Pow, 0, x)
    x = Symbol('x', zero=True)
    assert 0**-x == S.One
    assert 0**x == S.One

