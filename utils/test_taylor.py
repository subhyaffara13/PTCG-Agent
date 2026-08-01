
def test_taylor():
    mp.dps = 15
    # Easy to test since the coefficients are exact in floating-point
    assert taylor(sqrt, 1, 4) == [1, 0.5, -0.125, 0.0625, -0.0390625]

