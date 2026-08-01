
def test_large_unicode_characters(c1, c2):
    # c1 and c2 span ascii, 16bit and 32bit range.
    txt = StringIO(f"a,{c1},c,1.0\ne,{c2},2.0,g")
    res = np.loadtxt(txt, dtype=np.dtype('U12'), delimiter=",")
    expected = np.array(
        [f"a,{c1},c,1.0".split(","), f"e,{c2},2.0,g".split(",")],
        dtype=np.dtype('U12')
    )
    assert_equal(res, expected)

