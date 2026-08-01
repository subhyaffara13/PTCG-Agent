
def test_as_Basic():
    assert as_Basic(1) is S.One
    assert as_Basic(()) == Tuple()
    raises(TypeError, lambda: as_Basic([]))

