
def test_powers_Float():
    assert str((S('-1/10')**S('3/10')).n()) == str(Float(-.1)**(.3))

