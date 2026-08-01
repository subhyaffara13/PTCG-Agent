
def test_Domain_is_negative():
    I = S.ImaginaryUnit
    a, b = [CC.convert(x) for x in (2 + I, 5)]
    assert CC.is_negative(a) == False
    assert CC.is_negative(b) == False

