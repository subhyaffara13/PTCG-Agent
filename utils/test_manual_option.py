
def test_manual_option():
    raises(ValueError, lambda: integrate(1/x, x, manual=True, meijerg=True))
    # an example of a function that manual integration cannot handle
    assert integrate(log(1+x)/x, (x, 0, 1), manual=True).has(Integral)

