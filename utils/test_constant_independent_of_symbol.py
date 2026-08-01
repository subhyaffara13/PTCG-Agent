
def test_constant_independent_of_symbol():
    assert manualintegrate(Integral(y, (x, 1, 2)), x) == \
        x*Integral(y, (x, 1, 2))

