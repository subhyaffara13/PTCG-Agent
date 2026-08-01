
def test_ccode__isinf_isnan():
    assert ccode(isinf(x)) == 'isinf(x)'
    assert ccode(isnan(x)) == 'isnan(x)'

