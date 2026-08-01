
def test_scipy_threadpoolctl_version():
    check_threadpoolctl()

    import threadpoolctl

    # Ensure the extension module _fmm_core is loaded.
    from scipy.io._fast_matrix_market import _fmm_core
    with threadpoolctl.threadpool_limits(limits=4, user_api='scipy'):
        ctls = threadpoolctl.threadpool_info()
        for ctl in ctls:
            if ctl['user_api'] == 'scipy' and ctl['internal_api'] == 'scipy_mmio':
                assert ctl['version'] == _fmm_core.__version__

