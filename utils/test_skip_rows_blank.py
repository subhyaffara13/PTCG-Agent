
def test_skip_rows_blank(all_parsers):
    # see gh-9832
    parser = all_parsers
    text = """#foo,a,b,c
#foo,a,b,c

#foo,a,b,c
#foo,a,b,c

1/1/2000,1.,2.,3.
1/2/2000,4,5,6
1/3/2000,7,8,9
"""
    data = parser.read_csv(
        StringIO(text), skiprows=6, header=None, index_col=0, parse_dates=True
    )
    index = Index(
        [datetime(2000, 1, 1), datetime(2000, 1, 2), datetime(2000, 1, 3)],
        dtype="M8[us]",
        name=0,
    )

    expected = DataFrame(
        np.arange(1.0, 10.0).reshape((3, 3)), columns=[1, 2, 3], index=index
    )
    tm.assert_frame_equal(data, expected)

