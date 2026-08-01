
def test_resample_no_index(keys):
    # GH 47705
    df = DataFrame([], columns=["a", "b", "date"])
    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    result = df.groupby(keys).resample(rule=pd.to_timedelta("00:00:01")).mean()
    expected_columns = ["b"] if keys == ["a"] else []
    expected = DataFrame(columns=["a", "b", "date"]).set_index(keys, drop=False)
    expected["date"] = pd.to_datetime(expected["date"])
    expected = expected.set_index("date", append=True, drop=True)[expected_columns]
    if len(keys) == 1:
        expected.index.name = keys[0]

    tm.assert_frame_equal(result, expected)

