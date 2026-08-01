
def test_exception_noninteger_row_limits(param):
    with pytest.raises(TypeError, match="argument must be an integer"):
        np.loadtxt("foo.bar", **{param: 1.0})

