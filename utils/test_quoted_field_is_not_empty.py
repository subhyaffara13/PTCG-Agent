
def test_quoted_field_is_not_empty():
    txt = StringIO('1\n\n"4"\n""')
    expected = np.array(["1", "4", ""], dtype="U1")
    res = np.loadtxt(txt, delimiter=",", dtype="U1", quotechar='"')
    assert_equal(res, expected)

