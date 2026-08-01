
def test_Domain_is_nonpositive():
    I = S.ImaginaryUnit
    a, b = [CC.convert(x) for x in (2 + I, 5)]
    assert CC.is_nonpositive(a) == False
    assert CC.is_nonpositive(b) == False

