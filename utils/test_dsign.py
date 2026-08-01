
def test_dsign():
    x = Symbol('x')
    assert unchanged(dsign, 1, x)
    assert fcode(dsign(literal_dp(1), x), standard=95, source_format='free') == 'dsign(1d0, x)'

