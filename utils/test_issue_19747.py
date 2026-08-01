
def test_issue_19747():
    # test that negative k does not raise an error in nbinom.logcdf
    result = nbinom.logcdf([5, -1, 1], 5, 0.5)
    reference = [-0.47313352, -np.inf, -2.21297293]
    assert_allclose(result, reference)

