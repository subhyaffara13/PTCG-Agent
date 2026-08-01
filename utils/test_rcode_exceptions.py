
def test_rcode_exceptions():
    assert rcode(ceiling(x)) == "ceiling(x)"
    assert rcode(Abs(x)) == "abs(x)"
    assert rcode(gamma(x)) == "gamma(x)"

