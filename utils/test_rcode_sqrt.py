
def test_rcode_sqrt():
    assert rcode(sqrt(x)) == "sqrt(x)"
    assert rcode(x**0.5) == "sqrt(x)"
    assert rcode(sqrt(x)) == "sqrt(x)"

