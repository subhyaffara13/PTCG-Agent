
def test_fwf_colspecs_infer_nrows(infer_nrows, exp_data):
    # see gh-15138
    data = """\
  1  2
123 98
"""
    expected = DataFrame(exp_data)

    result = read_fwf(StringIO(data), infer_nrows=infer_nrows, header=None)
    tm.assert_frame_equal(result, expected)

