
def test_timestamp_groupby_quantile(unit):
    # GH 33168
    dti = pd.date_range(
        start="2020-04-19 00:00:00", freq="1min", periods=100, tz="UTC", unit=unit
    ).floor("1h")
    df = DataFrame(
        {
            "timestamp": dti,
            "category": list(range(1, 101)),
            "value": list(range(101, 201)),
        }
    )

    result = df.groupby("timestamp").quantile([0.2, 0.8])

    mi = pd.MultiIndex.from_product([dti[::99], [0.2, 0.8]], names=("timestamp", None))
    expected = DataFrame(
        [
            {"category": 12.8, "value": 112.8},
            {"category": 48.2, "value": 148.2},
            {"category": 68.8, "value": 168.8},
            {"category": 92.2, "value": 192.2},
        ],
        index=mi,
    )

    tm.assert_frame_equal(result, expected)

