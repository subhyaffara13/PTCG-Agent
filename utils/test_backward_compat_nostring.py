
def test_backward_compat_nostring(version, datapath):
    # The Stata data format prior to 105 did not support a date format
    # so read the raw values for comparison
    ref = datapath("io", "data", "stata", "stata-compat-118.dta")
    old = datapath("io", "data", "stata", f"stata-compat-{version}.dta")
    expected = read_stata(ref, convert_dates=False)
    # The Stata data format prior to 103 did not support string data
    expected = expected.drop(columns=["s10"])
    old_dta = read_stata(old, convert_dates=False)
    tm.assert_frame_equal(old_dta, expected, check_dtype=False)

