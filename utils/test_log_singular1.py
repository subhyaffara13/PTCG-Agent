
def test_log_singular1():
    assert log(1 + 1/x).nseries(x, n=5) == x - log(x) - x**2/2 + x**3/3 - \
        x**4/4 + O(x**5)

