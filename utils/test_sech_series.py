
def test_sech_series():
    x = Symbol('x')
    assert sech(x).series(x, 0, 10) == \
        1 - x**2/2 + 5*x**4/24 - 61*x**6/720 + 277*x**8/8064 + O(x**10)

