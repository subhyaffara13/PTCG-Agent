
def test_Domain_is_positive():
    I = S.ImaginaryUnit
    a, b = [CC.convert(x) for x in (2 + I, 5)]
    assert CC.is_positive(a) == False
    assert CC.is_positive(b) == False

