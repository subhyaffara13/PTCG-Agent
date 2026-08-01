
def test_L6():
    assert (log(tan(x/2 + pi/4)) - asinh(tan(x))).diff(x).subs({x: 0}) == 0

