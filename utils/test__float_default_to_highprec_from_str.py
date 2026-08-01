
def test_Float_default_to_highprec_from_str():
    s = str(pi.evalf(128))
    assert same_and_same_prec(Float(s), Float(s, ''))

