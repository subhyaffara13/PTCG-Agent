
def test_mi_data_columns(temp_hdfstore):
    # GH 14435
    idx = MultiIndex.from_arrays(
        [date_range("2000-01-01", periods=5), range(5)], names=["date", "id"]
    )
    df = DataFrame({"a": [1.1, 1.2, 1.3, 1.4, 1.5]}, index=idx)

    temp_hdfstore.append("df", df, data_columns=True)

    actual = temp_hdfstore.select("df", where="id == 1")
    expected = df.iloc[[1], :]
    tm.assert_frame_equal(actual, expected)

