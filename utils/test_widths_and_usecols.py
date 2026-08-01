
def test_widths_and_usecols():
    # GH#46580
    data = """0  1    n -0.4100.1
0  2    p  0.2 90.1
0  3    n -0.3140.4"""
    result = read_fwf(
        StringIO(data),
        header=None,
        usecols=(0, 1, 3),
        widths=(3, 5, 1, 5, 5),
        index_col=False,
        names=("c0", "c1", "c3"),
    )
    expected = DataFrame(
        {
            "c0": 0,
            "c1": [1, 2, 3],
            "c3": [-0.4, 0.2, -0.3],
        }
    )
    tm.assert_frame_equal(result, expected)

