
def test_groupby_any_with_timedelta():
    # GH#59712
    df = DataFrame({"value": [pd.Timedelta(1), pd.NaT]})

    result = df.groupby(np.array([0, 1], dtype=np.int64))["value"].any()

    expected = Series({0: True, 1: False}, name="value", dtype=bool)
    expected.index = expected.index.astype(np.int64)

    tm.assert_series_equal(result, expected)

