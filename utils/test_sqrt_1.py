
def test_sqrt_1():
    assert sqrt(1 + x).nseries(x, n=5) == 1 + x/2 - x**2/8 + x**3/16 - 5*x**4/128 + O(x**5)

