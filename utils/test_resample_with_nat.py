
def test_resample_with_nat(unit):
    # GH 13020
    index = DatetimeIndex(
        [
            pd.NaT,
            "1970-01-01 00:00:00",
            pd.NaT,
            "1970-01-01 00:00:01",
            "1970-01-01 00:00:02",
        ]
    ).as_unit(unit)
    frame = DataFrame([2, 3, 5, 7, 11], index=index)

    index_1s = DatetimeIndex(
        ["1970-01-01 00:00:00", "1970-01-01 00:00:01", "1970-01-01 00:00:02"]
    ).as_unit(unit)
    frame_1s = DataFrame([3.0, 7.0, 11.0], index=index_1s)
    tm.assert_frame_equal(frame.resample("1s").mean(), frame_1s)

    index_2s = DatetimeIndex(["1970-01-01 00:00:00", "1970-01-01 00:00:02"]).as_unit(
        unit
    )
    frame_2s = DataFrame([5.0, 11.0], index=index_2s)
    tm.assert_frame_equal(frame.resample("2s").mean(), frame_2s)

    index_3s = DatetimeIndex(["1970-01-01 00:00:00"]).as_unit(unit)
    frame_3s = DataFrame([7.0], index=index_3s)
    tm.assert_frame_equal(frame.resample("3s").mean(), frame_3s)

    tm.assert_frame_equal(frame.resample("60s").mean(), frame_3s)


def test_resample_with_nat():
    # GH 13223
    index = pd.to_timedelta(["0s", pd.NaT, "2s"])
    result = DataFrame({"value": [2, 3, 5]}, index).resample("1s").mean()
    expected = DataFrame(
        {"value": [2.5, np.nan, 5.0]},
        index=timedelta_range("0 day", periods=3, freq="1s"),
    )
    tm.assert_frame_equal(result, expected)

