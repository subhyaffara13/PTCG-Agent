
def test_merge_join_cols_error_reporting_duplicates(func, kwargs, err_msg):
    # GH: 16228
    left = DataFrame({"a": [1, 2], "b": [3, 4]})
    right = DataFrame({"a": [1, 1], "c": [5, 6]})
    msg = rf'Can only pass argument "{err_msg[0]}" OR "{err_msg[1]}" not both\.'
    with pytest.raises(MergeError, match=msg):
        getattr(pd, func)(left, right, **kwargs)

