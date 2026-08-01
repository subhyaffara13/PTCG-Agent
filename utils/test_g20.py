
def test_G20():
    s = symbols('s', integer=True, positive=True)
    # Wester erroneously has this as -s + sqrt(s**2 + 1)
    assert cf_r([[2*s]]) == s + sqrt(s**2 + 1)

