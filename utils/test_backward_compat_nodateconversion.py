
def test_backward_compat_nodateconversion(version, datapath):
    # The Stata data format prior to 105 did not support a date format
    # so read the raw values for comparison
    data_base = datapath("io", "data", "stata")
    ref = os.path.join(data_base, "stata-compat-118.dta")
    old = os.path.join(data_base, f"stata-compat-{version}.dta")
    expected = read_stata(ref, convert_dates=False)
    old_dta = read_stata(old, convert_dates=False)
    tm.assert_frame_equal(old_dta, expected, check_dtype=False)

