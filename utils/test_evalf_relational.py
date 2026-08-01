
def test_evalf_relational():
    assert Eq(x/5, y/10).evalf() == Eq(0.2*x, 0.1*y)
    # if this first assertion fails it should be replaced with
    # one that doesn't
    assert unchanged(Eq, (3 - I)**2/2 + I, 0)
    assert Eq((3 - I)**2/2 + I, 0).n() is S.false
    assert nfloat(Eq((3 - I)**2 + I, 0)) == S.false

