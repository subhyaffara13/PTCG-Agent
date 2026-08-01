
def test_mul_0():
    assert (x*log(x)).nseries(x, n=5) == x*log(x)

