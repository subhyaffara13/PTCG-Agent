
def test_orcsd_uncsd_lwork(dtype_, m):
    rng = np.random.default_rng(1234)
    p = rng.integers(0, m)
    q = m - p
    pfx = 'or' if dtype_ in REAL_DTYPES else 'un'
    dlw = pfx + 'csd_lwork'
    lw = get_lapack_funcs(dlw, dtype=dtype_)
    lwval = _compute_lwork(lw, m, p, q)
    lwval = lwval if pfx == 'un' else (lwval,)
    assert all([x > 0 for x in lwval])

