
def test_default_delimiter():
    header = None
    csv_data = """
a,bbb
cc,dd"""

    fwf_data = """
a \tbbb
cc\tdd """
    result = read_fwf(StringIO(fwf_data), widths=[3, 3], header=header, skiprows=[0])
    expected = read_csv(StringIO(csv_data), header=header)
    tm.assert_frame_equal(result, expected)

