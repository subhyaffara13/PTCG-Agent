
def test_dev0_a_b_rc_mixed():
    assert_(NumpyVersion('1.9.0a2.dev0+f16acvda') == '1.9.0a2.dev0+11111111')
    assert_(NumpyVersion('1.9.0a2.dev0+6acvda54') < '1.9.0a2')

