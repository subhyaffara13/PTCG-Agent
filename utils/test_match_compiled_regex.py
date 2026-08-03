import re

def test_match_compiled_regex(any_string_dtype):
    # GH#61952
    expected_dtype = (
        np.bool_ if is_object_or_nan_string_dtype(any_string_dtype) else "boolean"
    )

    values = Series(["ab", "AB", "abc", "ABC"], dtype=any_string_dtype)

    result = values.str.match(re.compile("ab"))
    expected = Series([True, False, True, False], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    msg = (
        "Cannot both specify 'case' and pass a compiled "
        "regexp object with conflicting case-sensitivity"
    )
    with pytest.raises(ValueError, match=msg):
        values.str.match(re.compile("ab"), case=False)

    result = values.str.match(re.compile("ab", flags=re.IGNORECASE))
    expected = Series([True, True, True, True], dtype=expected_dtype)
    tm.assert_series_equal(result, expected)

    msg = (
        "Cannot both specify 'flags' and pass a compiled "
        "regexp object with conflicting flags"
    )
    with pytest.raises(ValueError, match=msg):
        values.str.match(re.compile("ab"), flags=re.IGNORECASE)

    # But if the flags match you're OK
    values.str.match(re.compile("ab", flags=re.IGNORECASE), flags=re.IGNORECASE)

