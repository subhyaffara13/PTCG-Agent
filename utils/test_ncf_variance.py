
def test_ncf_variance():
    # Regression test for gh-10658 (incorrect variance formula for ncf).
    # The correct value of ncf.var(2, 6, 4), 42.75, can be verified with, for
    # example, Wolfram Alpha with the expression
    #     Variance[NoncentralFRatioDistribution[2, 6, 4]]
    # or with the implementation of the noncentral F distribution in the C++
    # library Boost.
    v = stats.ncf.var(2, 6, 4)
    assert_allclose(v, 42.75, rtol=1e-14)

