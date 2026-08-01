
def test_agg_timezone_round_trip():
    # GH 15426
    ts = pd.Timestamp("2016-01-01 12:00:00", tz="US/Pacific")
    df = DataFrame({"a": 1, "b": [ts + dt.timedelta(minutes=nn) for nn in range(10)]})

    result1 = df.groupby("a")["b"].agg("min").iloc[0]
    result2 = df.groupby("a")["b"].agg(lambda x: np.min(x)).iloc[0]
    result3 = df.groupby("a")["b"].min().iloc[0]

    assert result1 == ts
    assert result2 == ts
    assert result3 == ts

    dates = [
        pd.Timestamp(f"2016-01-0{i:d} 12:00:00", tz="US/Pacific") for i in range(1, 5)
    ]
    df = DataFrame({"A": ["a", "b"] * 2, "B": dates})
    grouped = df.groupby("A")

    ts = df["B"].iloc[0]
    assert ts == grouped.nth(0)["B"].iloc[0]
    assert ts == grouped.head(1)["B"].iloc[0]
    assert ts == grouped.first()["B"].iloc[0]

    # GH#27110 applying iloc should return a DataFrame
    assert ts == grouped.apply(lambda x: x.iloc[0])["B"].iloc[0]

    ts = df["B"].iloc[2]
    assert ts == grouped.last()["B"].iloc[0]

    # GH#27110 applying iloc should return a DataFrame
    assert ts == grouped.apply(lambda x: x.iloc[-1])["B"].iloc[0]

