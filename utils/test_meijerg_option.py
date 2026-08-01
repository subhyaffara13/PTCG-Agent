
def test_meijerg_option():
    raises(ValueError, lambda: integrate(1/x, x, meijerg=True, risch=True))
    # an example of a function that meijerg integration cannot handle
    assert integrate(tan(x), x, meijerg=True) == Integral(tan(x), x)

