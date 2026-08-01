
def test_version_1_point_10():
    # regression test for gh-2998.
    assert_(NumpyVersion('1.9.0') < '1.10.0')
    assert_(NumpyVersion('1.11.0') < '1.11.1')
    assert_(NumpyVersion('1.11.0') == '1.11.0')
    assert_(NumpyVersion('1.99.11') < '1.99.12')

