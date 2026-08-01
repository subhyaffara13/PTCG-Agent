
def test_downsample_dst_at_midnight(unit):
    # GH 25758
    start = datetime(2018, 11, 3, 12)
    end = datetime(2018, 11, 5, 12)
    index = date_range(start, end, freq="1h").as_unit(unit)
    index = index.tz_localize("UTC").tz_convert("America/Havana")
    data = list(range(len(index)))
    dataframe = DataFrame(data, index=index)
    result = dataframe.groupby(Grouper(freq="1D")).mean()

    dti = date_range("2018-11-03", periods=3).tz_localize(
        "America/Havana", ambiguous=True
    )
    dti = DatetimeIndex(dti, freq="D").as_unit(unit)
    expected = DataFrame([7.5, 28.0, 44.5], index=dti)
    tm.assert_frame_equal(result, expected)

