
def test_add_prefix_suffix_axis(string_series):
    # GH 47819
    with_prefix = string_series.add_prefix("foo#", axis=0)
    expected = Index([f"foo#{c}" for c in string_series.index])
    tm.assert_index_equal(with_prefix.index, expected)

    with_pct_suffix = string_series.add_suffix("#foo", axis=0)
    expected = Index([f"{c}#foo" for c in string_series.index])
    tm.assert_index_equal(with_pct_suffix.index, expected)


def test_add_prefix_suffix_axis(float_frame):
    # GH 47819
    with_prefix = float_frame.add_prefix("foo#", axis=0)
    expected = Index([f"foo#{c}" for c in float_frame.index])
    tm.assert_index_equal(with_prefix.index, expected)

    with_prefix = float_frame.add_prefix("foo#", axis=1)
    expected = Index([f"foo#{c}" for c in float_frame.columns])
    tm.assert_index_equal(with_prefix.columns, expected)

    with_pct_suffix = float_frame.add_suffix("#foo", axis=0)
    expected = Index([f"{c}#foo" for c in float_frame.index])
    tm.assert_index_equal(with_pct_suffix.index, expected)

    with_pct_suffix = float_frame.add_suffix("#foo", axis=1)
    expected = Index([f"{c}#foo" for c in float_frame.columns])
    tm.assert_index_equal(with_pct_suffix.columns, expected)

