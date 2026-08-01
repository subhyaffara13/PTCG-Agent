
def test_dev_version():
    assert_(NumpyVersion('1.9.0.dev-Unknown') < '1.9.0')
    for ver in ['1.9.0', '1.9.0a1', '1.9.0b2', '1.9.0b2.dev-ffffffff']:
        assert_(NumpyVersion('1.9.0.dev-f16acvda') < ver)

    assert_(NumpyVersion('1.9.0.dev-f16acvda') == '1.9.0.dev-11111111')

