
def test_partial_string_timestamp_multiindex_str_key_raises(df):
    # Even though this syntax works on a single index, this is somewhat
    # ambiguous and we don't want to extend this behavior forward to work
    # in multi-indexes. This would amount to selecting a scalar from a
    # column.
    with pytest.raises(KeyError, match="'2016-01-01'"):
        df["2016-01-01"]

