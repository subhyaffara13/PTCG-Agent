
def test_fwf_thousands(thousands):
    data = """\
 1 2,334.0    5
10   13     10.
"""
    data = data.replace(",", thousands)

    colspecs = [(0, 3), (3, 11), (12, 16)]
    expected = DataFrame([[1, 2334.0, 5], [10, 13, 10.0]])

    result = read_fwf(
        StringIO(data), header=None, colspecs=colspecs, thousands=thousands
    )
    tm.assert_almost_equal(result, expected)

