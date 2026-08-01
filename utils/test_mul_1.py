
def test_mul_1():
    assert (x*log(2 + x)).nseries(x, n=5) == x*log(2) + x**2/2 - x**3/8 + \
        x**4/24 + O(x**5)
    assert (x*log(1 + x)).nseries(
        x, n=5) == x**2 - x**3/2 + x**4/3 + O(x**5)

