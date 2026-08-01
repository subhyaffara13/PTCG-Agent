
def test_usecols_relative_to_names2(all_parsers):
    # see gh-5766
    data = """\
1,2,3
4,5,6
7,8,9
10,11,12"""
    parser = all_parsers

    result = parser.read_csv(
        StringIO(data), names=["a", "b"], header=None, usecols=[0, 1]
    )

    expected = DataFrame([[1, 2], [4, 5], [7, 8], [10, 11]], columns=["a", "b"])
    tm.assert_frame_equal(result, expected)

