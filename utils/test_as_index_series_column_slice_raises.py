
def test_as_index_series_column_slice_raises(df):
    # GH15072
    grouped = df.groupby("A", as_index=False)
    msg = r"Column\(s\) C already selected"

    with pytest.raises(IndexError, match=msg):
        grouped["C"].__getitem__("D")

