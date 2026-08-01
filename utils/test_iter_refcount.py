
def test_iter_refcount():
    # Make sure the iterator doesn't leak

    # Basic
    a = arange(6)
    dt = np.dtype('f4').newbyteorder()
    rc_a = sys.getrefcount(a)
    rc_dt = sys.getrefcount(dt)
    with nditer(a, [],
                [['readwrite', 'updateifcopy']],
                casting='unsafe',
                op_dtypes=[dt]) as it:
        assert_(not it.iterationneedsapi)
        assert_(sys.getrefcount(a) > rc_a)
        assert_(sys.getrefcount(dt) > rc_dt)
    # del 'it'
    it = None
    assert_equal(sys.getrefcount(a), rc_a)
    assert_equal(sys.getrefcount(dt), rc_dt)

    # With a copy
    a = arange(6, dtype='f4')
    dt = np.dtype('f4')
    rc_a = sys.getrefcount(a)
    rc_dt = sys.getrefcount(dt)
    it = nditer(a, [],
                [['readwrite']],
                op_dtypes=[dt])
    rc2_a = sys.getrefcount(a)
    rc2_dt = sys.getrefcount(dt)
    it2 = it.copy()
    assert_(sys.getrefcount(a) > rc2_a)
    if sys.version_info < (3, 13):
        # np.dtype('f4') is immortal after Python 3.13
        assert_(sys.getrefcount(dt) > rc2_dt)
    it = None
    assert_equal(sys.getrefcount(a), rc2_a)
    assert_equal(sys.getrefcount(dt), rc2_dt)
    it2 = None
    assert_equal(sys.getrefcount(a), rc_a)
    assert_equal(sys.getrefcount(dt), rc_dt)

