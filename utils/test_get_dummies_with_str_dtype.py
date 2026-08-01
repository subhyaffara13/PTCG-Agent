
def test_get_dummies_with_str_dtype(any_string_dtype):
    s = Series(["a|b", "a|c", np.nan], dtype=any_string_dtype)

    msg = "Only numeric or boolean dtypes are supported for 'dtype'"
    with pytest.raises(ValueError, match=msg):
        s.str.get_dummies("|", dtype=str)

    with pytest.raises(ValueError, match=msg):
        s.str.get_dummies("|", dtype="datetime64[ns]")

