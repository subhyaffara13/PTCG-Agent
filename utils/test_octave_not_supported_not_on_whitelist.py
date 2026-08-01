
def test_octave_not_supported_not_on_whitelist():
    from sympy.functions.special.polynomials import assoc_laguerre
    with raises(NotImplementedError):
        mcode(assoc_laguerre(x, y, z))

