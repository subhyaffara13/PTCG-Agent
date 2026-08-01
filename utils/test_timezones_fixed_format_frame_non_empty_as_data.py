
def test_timezones_fixed_format_frame_non_empty_as_data(temp_hdfstore):
    # GH11411
    rng = date_range("1/1/2000", "1/30/2000", tz="US/Eastern")
    rng = rng._with_freq(None)  # freq doesn't round-trip
    df = DataFrame(
        {
            "A": rng,
            "B": rng.tz_convert("UTC").tz_localize(None),
            "C": rng.tz_convert("CET"),
            "D": range(len(rng)),
        },
        index=rng,
    )
    temp_hdfstore["df"] = df
    result = temp_hdfstore["df"]
    tm.assert_frame_equal(result, df)

