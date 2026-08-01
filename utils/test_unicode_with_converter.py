
def test_unicode_with_converter():
    txt = StringIO("cat,dog\nαβγ,δεζ\nabc,def\n")
    conv = {0: lambda s: s.upper()}
    res = np.loadtxt(
        txt,
        dtype=np.dtype("U12"),
        converters=conv,
        delimiter=",",
        encoding=None
    )
    expected = np.array([['CAT', 'dog'], ['ΑΒΓ', 'δεζ'], ['ABC', 'def']])
    assert_equal(res, expected)

