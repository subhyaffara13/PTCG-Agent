
def test_threadpoolctl():
    check_threadpoolctl()

    import threadpoolctl

    # Ensure the extension module _fmm_core is loaded.
    from scipy.io._fast_matrix_market import _fmm_core  # noqa: F401

    with threadpoolctl.threadpool_limits(limits=4):
        assert_equal(fmm.PARALLELISM, 4)

    with threadpoolctl.threadpool_limits(limits=2, user_api='scipy'):
        assert_equal(fmm.PARALLELISM, 2)

