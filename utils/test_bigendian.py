
def test_bigendian(version, datapath):
    ref = datapath("io", "data", "stata", f"stata-compat-{version}.dta")
    big = datapath("io", "data", "stata", f"stata-compat-be-{version}.dta")
    expected = read_stata(ref)
    big_dta = read_stata(big)
    tm.assert_frame_equal(big_dta, expected)

