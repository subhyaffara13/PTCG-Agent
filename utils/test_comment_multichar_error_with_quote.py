
def test_comment_multichar_error_with_quote():
    txt = StringIO("1,2\n3,4")
    msg = (
        "when multiple comments or a multi-character comment is given, "
        "quotes are not supported."
    )
    with pytest.raises(ValueError, match=msg):
        np.loadtxt(txt, delimiter=",", comments="123", quotechar='"')
    with pytest.raises(ValueError, match=msg):
        np.loadtxt(txt, delimiter=",", comments=["#", "%"], quotechar='"')

    # A single character string in a tuple is unpacked though:
    res = np.loadtxt(txt, delimiter=",", comments=("#",), quotechar="'")
    assert_equal(res, [[1, 2], [3, 4]])

