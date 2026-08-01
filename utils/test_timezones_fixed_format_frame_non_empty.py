
def test_timezones_fixed_format_frame_non_empty(temp_hdfstore):
    # index
    rng = date_range("1/1/2000", "1/30/2000", tz="US/Eastern")
    rng = rng._with_freq(None)  # freq doesn't round-trip
    df = DataFrame(np.random.default_rng(2).standard_normal((len(rng), 4)), index=rng)
    temp_hdfstore["df"] = df
    result = temp_hdfstore["df"]
    tm.assert_frame_equal(result, df)

