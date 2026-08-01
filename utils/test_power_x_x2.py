
def test_power_x_x2():
    assert (x**x).nseries(x, n=4) == \
        1 + x*log(x) + x**2*log(x)**2/2 + x**3*log(x)**3/6 + O(x**4*log(x)**4)

