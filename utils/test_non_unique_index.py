
def test_non_unique_index():
    # GH 16577
    df = DataFrame(
        {"A": [1.0, 2.0, 3.0, np.nan], "value": 1.0},
        index=[pd.Timestamp("20170101", tz="US/Eastern")] * 4,
    )
    result = df.groupby([df.index, "A"]).value.rank(ascending=True, pct=True)
    expected = Series(
        [1.0, 1.0, 1.0, np.nan],
        index=[pd.Timestamp("20170101", tz="US/Eastern")] * 4,
        name="value",
    )
    tm.assert_series_equal(result, expected)

