
def test_ccode_exceptions():
    assert ccode(gamma(x), standard='C99') == "tgamma(x)"
    with raises(PrintMethodNotImplementedError):
        ccode(gamma(x), standard='C89')
    with raises(PrintMethodNotImplementedError):
        ccode(gamma(x), standard='C89', allow_unknown_functions=False)

    ccode(gamma(x), standard='C89', allow_unknown_functions=True)

