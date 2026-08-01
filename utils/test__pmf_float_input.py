
def test__pmf_float_input():
    # gh-21272
    # test that `rvs()` can be computed when `_pmf` requires float input

    class rv_exponential(stats.rv_discrete):
        def _pmf(self, i):
            return (2/3)*3**(1 - i)

    rv = rv_exponential(a=0.0, b=float('inf'))
    rvs = rv.rvs(random_state=42)  # should not crash due to integer input to `_pmf`
    assert_allclose(rvs, 0)

