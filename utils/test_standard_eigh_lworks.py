
def test_standard_eigh_lworks(pfx, driver):
    n = 1200  # Some sufficiently big arbitrary number
    dtype = REAL_DTYPES if pfx == 'sy' else COMPLEX_DTYPES
    sc_dlw = get_lapack_funcs(pfx+driver+'_lwork', dtype=dtype[0])
    dz_dlw = get_lapack_funcs(pfx+driver+'_lwork', dtype=dtype[1])
    try:
        _compute_lwork(sc_dlw, n, lower=1)
        _compute_lwork(dz_dlw, n, lower=1)
    except Exception as e:
        pytest.fail(f"{pfx+driver}_lwork raised unexpected exception: {e}")

