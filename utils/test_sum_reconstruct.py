
def test_sum_reconstruct():
    s = Sum(n**2, (n, -1, 1))
    assert s == Sum(*s.args)
    raises(ValueError, lambda: Sum(x, x))
    raises(ValueError, lambda: Sum(x, (x, 1)))

