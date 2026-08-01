
def test_bigendian_nodateconversion(version, datapath):
    # The Stata data format prior to 105 did not support a date format
    # so read the raw values for comparison
    ref = datapath("io", "data", "stata", f"stata-compat-{version}.dta")
    big = datapath("io", "data", "stata", f"stata-compat-be-{version}.dta")
    expected = read_stata(ref, convert_dates=False)
    big_dta = read_stata(big, convert_dates=False)
    tm.assert_frame_equal(big_dta, expected)

