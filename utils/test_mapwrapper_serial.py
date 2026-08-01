
def test_mapwrapper_serial():
    in_arg = np.arange(10.)
    out_arg = np.sin(in_arg)

    p = MapWrapper(1)
    assert_(p._mapfunc is map)
    assert_(p.pool is None)
    assert_(p._own_pool is False)
    out = list(p(np.sin, in_arg))
    assert_equal(out, out_arg)

    with assert_raises(RuntimeError):
        p = MapWrapper(0)

