
def test_apply_aggregating_timedelta_and_datetime():
    # Regression test for GH 15562
    # The following groupby caused ValueErrors and IndexErrors pre 0.20.0

    df = DataFrame(
        {
            "clientid": ["A", "B", "C"],
            "datetime": [np.datetime64("2017-02-01 00:00:00")] * 3,
        }
    )
    df["time_delta_zero"] = df.datetime - df.datetime
    result = df.groupby("clientid").apply(
        lambda ddf: Series(
            {"clientid_age": ddf.time_delta_zero.min(), "date": ddf.datetime.min()}
        )
    )
    expected = DataFrame(
        {
            "clientid": ["A", "B", "C"],
            "clientid_age": [np.timedelta64(0, "D")] * 3,
            "date": [np.datetime64("2017-02-01 00:00:00")] * 3,
        }
    ).set_index("clientid")

    tm.assert_frame_equal(result, expected)

