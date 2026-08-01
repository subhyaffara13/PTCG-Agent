
def test_whitespace_preservation():
    # see gh-16772
    header = None
    csv_data = """
 a ,bbb
 cc,dd """

    fwf_data = """
 a bbb
 ccdd """
    result = read_fwf(
        StringIO(fwf_data), widths=[3, 3], header=header, skiprows=[0], delimiter="\n\t"
    )
    expected = read_csv(StringIO(csv_data), header=header)
    tm.assert_frame_equal(result, expected)

