
def test_accum_bounds():
    assert limit_seq((-1)**n, n) == AccumulationBounds(-1, 1)
    assert limit_seq(cos(pi*n), n) == AccumulationBounds(-1, 1)
    assert limit_seq(sin(pi*n/2)**2, n) == AccumulationBounds(0, 1)
    assert limit_seq(2*(-3)**n/(n + 3**n), n) == AccumulationBounds(-2, 2)
    assert limit_seq(3*n/(n + 1) + 2*(-1)**n, n) == AccumulationBounds(1, 5)

