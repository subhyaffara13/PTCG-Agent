
def test_select_dtypes_timestamp(temp_hdfstore):
    # with a Timestamp data column (GH #2637)
    df = DataFrame(
        {
            "ts": bdate_range("2012-01-01", periods=300, unit="ns"),
            "A": np.random.default_rng(2).standard_normal(300),
        }
    )
    temp_hdfstore.append("df", df, data_columns=["ts", "A"])

    result = temp_hdfstore.select("df", "ts>=Timestamp('2012-02-01')")
    expected = df[df.ts >= Timestamp("2012-02-01")]
    tm.assert_frame_equal(expected, result)

