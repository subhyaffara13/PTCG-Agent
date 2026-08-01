
def test_issue_21971():
    a, b, c, d = symbols('a b c d')
    f = a & b & c | a & c
    assert f.subs(a & c, d) == b & d | d
    assert f.subs(a & b & c, d) == a & c | d

    f = (a | b | c) & (a | c)
    assert f.subs(a | c, d) == (b | d) & d
    assert f.subs(a | b | c, d) == (a | c) & d

    f = (a ^ b ^ c) & (a ^ c)
    assert f.subs(a ^ c, d) == (b ^ d) & d
    assert f.subs(a ^ b ^ c, d) == (a ^ c) & d

