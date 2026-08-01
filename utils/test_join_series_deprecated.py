
def test_join_series_deprecated():
    # GH#62897
    idx = pd.Index([1, 2])
    ser = pd.Series([1, 2, 2])
    with tm.assert_produces_warning(
        Pandas4Warning, match="Passing .* to .* is deprecated"
    ):
        idx.join(ser)

