
def test_bad_min_fname_arg_count(_fname):
    msg = "'max_fname_arg_count' must be non-negative"

    with pytest.raises(ValueError, match=msg):
        validate_args(_fname, (None,), -1, "foo")

