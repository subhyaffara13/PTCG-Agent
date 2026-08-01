
def test_log_power1():
    e = 1 / (1/x + x ** (log(3)/log(2)))
    assert e.nseries(x, n=5) == -x**(log(3)/log(2) + 2) + x + O(x**5)

