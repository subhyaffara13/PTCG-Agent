import os

def test_backward_compat(version, datapath):
    data_base = datapath("io", "data", "stata")
    ref = os.path.join(data_base, "stata-compat-118.dta")
    old = os.path.join(data_base, f"stata-compat-{version}.dta")
    expected = read_stata(ref)
    old_dta = read_stata(old)
    tm.assert_frame_equal(old_dta, expected, check_dtype=False)

