
def test_comment_multiple_chars(comment):
    content = "# IGNORE\n1.5, 2.5# ABC\n3.0,4.0# XXX\n5.5,6.0\n"
    txt = StringIO(content.replace("#", comment))
    a = np.loadtxt(txt, delimiter=",", comments=comment)
    assert_equal(a, [[1.5, 2.5], [3.0, 4.0], [5.5, 6.0]])

