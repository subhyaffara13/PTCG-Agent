
def test_boost_divide_by_zero_issue_15101():
    n = 1000
    p = 0.01
    k = 996
    assert_allclose(binom.pmf(k, n, p), 0.0)

