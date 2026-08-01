
def test_generalized_eigh_lworks(pfx, driver):
    n = 1200  # Some sufficiently big arbitrary number
    dtype = REAL_DTYPES if pfx == 'sy' else COMPLEX_DTYPES
    sc_dlw = get_lapack_funcs(pfx+driver+'_lwork', dtype=dtype[0])
    dz_dlw = get_lapack_funcs(pfx+driver+'_lwork', dtype=dtype[1])
    # Shouldn't raise any exceptions
    try:
        _compute_lwork(sc_dlw, n, uplo="L")
        _compute_lwork(dz_dlw, n, uplo="L")
    except Exception as e:
        pytest.fail(f"{pfx+driver}_lwork raised unexpected exception: {e}")

