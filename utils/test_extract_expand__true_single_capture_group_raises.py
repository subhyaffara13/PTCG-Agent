
def test_extract_expand_True_single_capture_group_raises(
    index_or_series, any_string_dtype
):
    # these should work for both Series and Index
    # no groups
    s_or_idx = index_or_series(["A1", "B2", "C3"], dtype=any_string_dtype)
    msg = "pattern contains no capture groups"
    with pytest.raises(ValueError, match=msg):
        s_or_idx.str.extract("[ABC][123]", expand=True)

    # only non-capturing groups
    with pytest.raises(ValueError, match=msg):
        s_or_idx.str.extract("(?:[AB]).*", expand=True)

