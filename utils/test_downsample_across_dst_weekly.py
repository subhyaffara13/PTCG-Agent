
def test_downsample_across_dst_weekly(unit):
    # GH 9119, GH 21459
    df = DataFrame(
        index=DatetimeIndex(
            ["2017-03-25", "2017-03-26", "2017-03-27", "2017-03-28", "2017-03-29"],
            tz="Europe/Amsterdam",
        ).as_unit(unit),
        data=[11, 12, 13, 14, 15],
    )
    result = df.resample("1W").sum()
    expected = DataFrame(
        [23, 42],
        index=DatetimeIndex(
            ["2017-03-26", "2017-04-02"], tz="Europe/Amsterdam", freq="W"
        ).as_unit(unit),
    )
    tm.assert_frame_equal(result, expected)

