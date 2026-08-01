
def test_infinities():
    assert oo.evalf(chop=True) == inf
    assert (-oo).evalf(chop=True) == ninf

