
def test_rcode_constants_mathh():
    assert rcode(exp(1)) == "exp(1)"
    assert rcode(pi) == "pi"
    assert rcode(oo) == "Inf"
    assert rcode(-oo) == "-Inf"

