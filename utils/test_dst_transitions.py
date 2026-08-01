
def test_dst_transitions(temp_hdfstore):
    # make sure we are not failing on transitions
    times = date_range(
        "2013-10-26 23:00",
        "2013-10-27 01:00",
        tz="Europe/London",
        freq="h",
        ambiguous="infer",
    )
    times = times._with_freq(None)  # freq doesn't round-trip

    for i in [times, times + pd.Timedelta("10min")]:
        df = DataFrame({"A": range(len(i)), "B": i}, index=i)
        temp_hdfstore.append("df", df)
        result = temp_hdfstore.select("df")
        tm.assert_frame_equal(result, df)
        temp_hdfstore.remove("df")

