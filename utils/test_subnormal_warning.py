
def test_subnormal_warning():
    """Test that the subnormal is zero warning is not being raised."""
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        # Test for common float types
        for dtype in [np.float16, np.float32, np.float64]:
            f = finfo(dtype)
            _ = f.smallest_subnormal
        # Also test longdouble
        with np.errstate(all='ignore'):
            fld = finfo(np.longdouble)
            _ = fld.smallest_subnormal
        # Check no warnings were raised
        assert len(w) == 0

