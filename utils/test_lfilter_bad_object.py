
def test_lfilter_bad_object(xp):
    # lfilter: object arrays with non-numeric objects raise TypeError.
    # Regression test for ticket #1452.
    if hasattr(sys, 'abiflags') and 'd' in sys.abiflags:
        pytest.skip('test is flaky when run with python3-dbg')
    assert_raises(TypeError, lfilter, [1.0], [1.0], [1.0, None, 2.0])
    assert_raises(TypeError, lfilter, [1.0], [None], [1.0, 2.0, 3.0])
    assert_raises(TypeError, lfilter, [None], [1.0], [1.0, 2.0, 3.0])

