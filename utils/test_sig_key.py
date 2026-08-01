
def test_sig_key():
    s1 = sig((0,) * 3, 2)
    s2 = sig((1,) * 3, 4)
    s3 = sig((2,) * 3, 2)

    assert sig_key(s1, lex) > sig_key(s2, lex)
    assert sig_key(s2, lex) < sig_key(s3, lex)

