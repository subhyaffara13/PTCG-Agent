
def test_mapwrapper_parallel():
    in_arg = np.arange(10.)
    out_arg = np.sin(in_arg)

    with MapWrapper(2) as p:
        out = p(np.sin, in_arg)
        assert_equal(list(out), out_arg)

        assert_(p._own_pool is True)
        assert_(isinstance(p.pool, PWL))
        assert_(p._mapfunc is not None)

    # the context manager should've closed the internal pool
    # check that it has by asking it to calculate again.
    with assert_raises(Exception) as excinfo:
        p(np.sin, in_arg)

    assert_(excinfo.type is ValueError)

    # can also set a PoolWrapper up with a map-like callable instance
    with Pool(2) as p:
        q = MapWrapper(p.map)

        assert_(q._own_pool is False)
        q.close()

        # closing the PoolWrapper shouldn't close the internal pool
        # because it didn't create it
        out = p.map(np.sin, in_arg)
        assert_equal(list(out), out_arg)

