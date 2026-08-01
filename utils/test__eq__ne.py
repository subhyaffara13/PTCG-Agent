
def test_Eq_Ne():

    assert Eq(x, x)  # issue 5719

    # issue 6116
    p = Symbol('p', positive=True)
    assert Eq(p, 0) is S.false

    # issue 13348; 19048
    # SymPy is strict about 0 and 1 not being
    # interpreted as Booleans
    assert Eq(True, 1) is S.false
    assert Eq(False, 0) is S.false
    assert Eq(~x, 0) is S.false
    assert Eq(~x, 1) is S.false
    assert Ne(True, 1) is S.true
    assert Ne(False, 0) is S.true
    assert Ne(~x, 0) is S.true
    assert Ne(~x, 1) is S.true

    assert Eq((), 1) is S.false
    assert Ne((), 1) is S.true

