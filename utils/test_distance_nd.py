
def test_distance_nd(func, p, weights):
    #  check that inputs broadcast correctly against a reference implementation
    rng = np.random.default_rng(6738657865438)
    ref_func = _apply_over_batch(('u', 1), ('v', 1), ('p', 1), ('w', 1))(func)

    u = rng.random((5, 2, 4))
    v = rng.random((2, 4))
    w = rng.random(4) if weights else None
    kwargs = {'w': w} if p is None else {'p': p, 'w': w}

    res = func(u, v, **kwargs)
    ref = ref_func(u, v, **kwargs)

    assert_allclose(res, ref)

