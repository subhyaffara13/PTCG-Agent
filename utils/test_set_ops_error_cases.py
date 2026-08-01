
def test_set_ops_error_cases(idx, case, sort, method):
    # non-iterable input
    msg = "Input must be Index or array-like"
    with pytest.raises(TypeError, match=msg):
        getattr(idx, method)(case, sort=sort)

