
def test_isign():
    x = Symbol('x', integer=True)
    assert unchanged(isign, 1, x)
    assert fcode(isign(1, x), standard=95, source_format='free') == 'isign(1, x)'

