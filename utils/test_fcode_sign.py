
def test_fcode_sign():  #issue 12267
    x=symbols('x')
    y=symbols('y', integer=True)
    z=symbols('z', complex=True)
    assert fcode(sign(x), standard=95, source_format='free') == "merge(0d0, dsign(1d0, x), x == 0d0)"
    assert fcode(sign(y), standard=95, source_format='free') == "merge(0, isign(1, y), y == 0)"
    assert fcode(sign(z), standard=95, source_format='free') == "merge(cmplx(0d0, 0d0), z/abs(z), abs(z) == 0d0)"
    raises(NotImplementedError, lambda: fcode(sign(x)))

