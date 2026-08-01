
def test_Float_RealElement():
    repi = RealField(dps=100)(pi.evalf(100))
    # We still have to pass the precision because Float doesn't know what
    # RealElement is, but make sure it keeps full precision from the result.
    assert Float(repi, 100) == pi.evalf(100)

