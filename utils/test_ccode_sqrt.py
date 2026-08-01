
def test_ccode_sqrt():
    assert ccode(sqrt(x)) == "sqrt(x)"
    assert ccode(x**0.5) == "sqrt(x)"
    assert ccode(sqrt(x)) == "sqrt(x)"

