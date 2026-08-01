
def test_Rational_as_content_primitive():
    c, p = S.One, S.Zero
    assert (c*p).as_content_primitive() == (c, p)
    c, p = S.Half, S.One
    assert (c*p).as_content_primitive() == (c, p)

