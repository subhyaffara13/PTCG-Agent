
def test_apply_series_return_dataframe_groups():
    # GH 10078
    tdf = DataFrame(
        {
            "day": {
                0: pd.Timestamp("2015-02-24 00:00:00"),
                1: pd.Timestamp("2015-02-24 00:00:00"),
                2: pd.Timestamp("2015-02-24 00:00:00"),
                3: pd.Timestamp("2015-02-24 00:00:00"),
                4: pd.Timestamp("2015-02-24 00:00:00"),
            },
            "userAgent": {
                0: "some UA string",
                1: "some UA string",
                2: "some UA string",
                3: "another UA string",
                4: "some UA string",
            },
            "userId": {
                0: "17661101",
                1: "17661101",
                2: "17661101",
                3: "17661101",
                4: "17661101",
            },
        }
    )

    def most_common_values(df):
        return Series({c: s.value_counts().index[0] for c, s in df.items()})

    result = tdf.groupby("day").apply(most_common_values)["userId"]
    expected = Series(
        ["17661101"], index=pd.DatetimeIndex(["2015-02-24"], name="day"), name="userId"
    )
    tm.assert_series_equal(result, expected)

