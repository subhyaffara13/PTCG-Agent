
def test_V4():
    assert integrate(2**x/sqrt(1 + 4**x), x) == asinh(2**x)/log(2)

