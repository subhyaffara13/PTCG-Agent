
def test_entropy():
    up = JzKet(S.Half, S.Half)
    down = JzKet(S.Half, Rational(-1, 2))
    d = Density((up, S.Half), (down, S.Half))

    # test for density object
    ent = entropy(d)
    assert entropy(d) == log(2)/2
    assert d.entropy() == log(2)/2

    np = import_module('numpy', min_module_version='1.4.0')
    if np:
        #do this test only if 'numpy' is available on test machine
        np_mat = represent(d, format='numpy')
        ent = entropy(np_mat)
        assert isinstance(np_mat, np.ndarray)
        assert ent.real == 0.69314718055994529
        assert ent.imag == 0

    scipy = import_module('scipy', import_kwargs={'fromlist': ['sparse']})
    if scipy and np:
        #do this test only if numpy and scipy are available
        mat = represent(d, format="scipy.sparse")
        assert isinstance(mat, scipy_sparse_matrix)
        assert ent.real == 0.69314718055994529
        assert ent.imag == 0


def test_entropy(nargs, dtype, xp, devices):
    dtype = getattr(xp, dtype)
    for device in devices:
        args = get_arrays(nargs, device=device, dtype=dtype, xp=xp)
        res = stats.entropy(*args)
        assert xp_device(res) == xp_device(args[0])
        assert res.dtype == dtype


def test_entropy(qk, base, axis, xp):
    mxp, marrays, narrays = get_arrays(2 if qk else 1, xp=xp)
    res = stats.entropy(*marrays, base=base, axis=axis)
    ref = stats.entropy(*narrays, base=base, nan_policy='omit', axis=axis)
    xp_assert_close(res.data, xp.asarray(ref))

