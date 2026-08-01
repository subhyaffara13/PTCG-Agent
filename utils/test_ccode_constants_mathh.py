
def test_ccode_constants_mathh():
    assert ccode(exp(1)) == "M_E"
    assert ccode(pi) == "M_PI"
    assert ccode(oo, standard='c89') == "HUGE_VAL"
    assert ccode(-oo, standard='c89') == "-HUGE_VAL"
    assert ccode(oo) == "INFINITY"
    assert ccode(-oo, standard='c99') == "-INFINITY"
    assert ccode(pi, type_aliases={real: float80}) == "M_PIl"

