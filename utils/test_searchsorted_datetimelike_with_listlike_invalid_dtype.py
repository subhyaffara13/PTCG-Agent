
def test_searchsorted_datetimelike_with_listlike_invalid_dtype(values, arg):
    # https://github.com/pandas-dev/pandas/issues/32762
    msg = "[Unexpected type|Cannot compare]"
    with pytest.raises(TypeError, match=msg):
        values.searchsorted(arg)

