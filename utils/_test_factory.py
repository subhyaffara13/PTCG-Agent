
def _test_factory(test, dtype=np.float64):
    """Boost test"""
    with warnings.catch_warnings():
        msg = "The occurrence of roundoff error is detected"
        warnings.filterwarnings("ignore", msg, IntegrationWarning)
        with np.errstate(all='ignore'):
            test.check(dtype=dtype)

