
def test_precision_loss(temp_file):
    df = DataFrame(
        [[sum(2**i for i in range(60)), sum(2**i for i in range(52))]],
        columns=["big", "little"],
    )
    with tm.assert_produces_warning(
        PossiblePrecisionLoss, match="Column converted from int64 to float64"
    ):
        df.to_stata(temp_file, write_index=False)
    reread = read_stata(temp_file)
    expected_dt = Series([np.float64, np.float64], index=["big", "little"])
    tm.assert_series_equal(reread.dtypes, expected_dt)
    assert reread.loc[0, "little"] == df.loc[0, "little"]
    assert reread.loc[0, "big"] == float(df.loc[0, "big"])

