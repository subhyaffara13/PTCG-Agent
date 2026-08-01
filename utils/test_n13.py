
def test_N13():
    x = Symbol('x')
    assert solveset(sin(x) < 2, domain=S.Reals) == S.Reals

