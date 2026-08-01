
def test_issue_8821_highprec_from_str():
    s = str(pi.evalf(128))
    p = N(s)
    assert Abs(sin(p)) < 1e-15
    p = N(s, 64)
    assert Abs(sin(p)) < 1e-64


def test_issue_8821_highprec_from_str():
    s = str(pi.evalf(128))
    p = sympify(s)
    assert Abs(sin(p)) < 1e-127

