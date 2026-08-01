
def test_with_dictlike_columns_with_datetime():
    # GH 18775
    df = DataFrame()
    df["author"] = ["X", "Y", "Z"]
    df["publisher"] = ["BBC", "NBC", "N24"]
    df["date"] = pd.to_datetime(
        ["17-10-2010 07:15:30", "13-05-2011 08:20:35", "15-01-2013 09:09:09"],
        dayfirst=True,
    )
    result = df.apply(lambda x: {}, axis=1)
    expected = Series([{}, {}, {}])
    tm.assert_series_equal(result, expected)

