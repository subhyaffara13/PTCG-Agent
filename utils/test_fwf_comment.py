
def test_fwf_comment(comment):
    data = """\
  1   2.   4  #hello world
  5  NaN  10.0
"""
    data = data.replace("#", comment)

    colspecs = [(0, 3), (4, 9), (9, 25)]
    expected = DataFrame([[1, 2.0, 4], [5, np.nan, 10.0]])

    result = read_fwf(StringIO(data), colspecs=colspecs, header=None, comment=comment)
    tm.assert_almost_equal(result, expected)

