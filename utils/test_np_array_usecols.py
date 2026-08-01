
def test_np_array_usecols(all_parsers):
    # see gh-12546
    parser = all_parsers
    data = "a,b,c\n1,2,3"
    usecols = np.array(["a", "b"])

    expected = DataFrame([[1, 2]], columns=usecols)
    result = parser.read_csv(StringIO(data), usecols=usecols)
    tm.assert_frame_equal(result, expected)

