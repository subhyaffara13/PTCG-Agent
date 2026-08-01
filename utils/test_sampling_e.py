
def test_samplingE():
    scipy = import_module('scipy')
    if not scipy:
        skip('Scipy is not installed. Abort tests')
    Y = Normal('Y', 0, 1)
    z = Symbol('z', integer=True)
    assert E(Sum(1/z**Y, (z, 1, oo)), Y > 2, numsamples=3).is_number

