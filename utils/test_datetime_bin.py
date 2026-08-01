
def test_datetime_bin(conv):
    data = [np.datetime64("2012-12-13"), np.datetime64("2012-12-15")]
    bin_data = ["2012-12-12", "2012-12-14", "2012-12-16"]

    expected = Series(
        IntervalIndex(
            [
                Interval(Timestamp(bin_data[0]), Timestamp(bin_data[1])),
                Interval(Timestamp(bin_data[1]), Timestamp(bin_data[2])),
            ]
        )
    )

    bins = [conv(v) for v in bin_data]
    result = Series(cut(data, bins=bins))

    if type(bins[0]) is np.datetime64:
        # The bins have microsecond dtype -> so does result
        expected = expected.astype("interval[datetime64[s]]")

    expected = expected.astype(CategoricalDtype(ordered=True))
    tm.assert_series_equal(result, expected)

