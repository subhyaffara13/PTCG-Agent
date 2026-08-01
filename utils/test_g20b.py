
def test_G20b():
    s = symbols('s', integer=True, positive=True)
    assert cf_p(s, 1, s**2 + 1) == [[2*s]]

