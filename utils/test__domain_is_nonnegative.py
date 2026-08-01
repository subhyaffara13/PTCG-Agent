
def test_Domain_is_nonnegative():
    I = S.ImaginaryUnit
    a, b = [CC.convert(x) for x in (2 + I, 5)]
    assert CC.is_nonnegative(a) == False
    assert CC.is_nonnegative(b) == False

