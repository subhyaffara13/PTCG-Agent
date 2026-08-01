
def test_fwf_colspecs_none(colspecs, exp_data):
    # see gh-7079
    data = """\
123456
456789
"""
    expected = DataFrame(exp_data)

    result = read_fwf(StringIO(data), colspecs=colspecs, header=None)
    tm.assert_frame_equal(result, expected)

