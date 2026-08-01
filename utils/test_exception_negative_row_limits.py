
def test_exception_negative_row_limits(param):
    """skiprows and max_rows should raise for negative parameters."""
    with pytest.raises(ValueError, match="argument must be nonnegative"):
        np.loadtxt("foo.bar", **{param: -3})

