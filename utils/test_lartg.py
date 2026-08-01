
def test_lartg():
    for dtype in 'fdFD':
        lartg = get_lapack_funcs('lartg', dtype=dtype)

        f = np.array(3, dtype)
        g = np.array(4, dtype)

        if np.iscomplexobj(g):
            g *= 1j

        cs, sn, r = lartg(f, g)

        assert_allclose(cs, 3.0/5.0)
        assert_allclose(r, 5.0)

        if np.iscomplexobj(g):
            assert_allclose(sn, -4.0j/5.0)
            assert_(isinstance(r, complex))
            assert_(isinstance(cs, float))
        else:
            assert_allclose(sn, 4.0/5.0)

