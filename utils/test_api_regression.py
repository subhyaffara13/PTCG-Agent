
def test_api_regression():
    # https://github.com/scipy/scipy/issues/3802
    _assert_hasattr(scipy.stats.distributions, 'f_gen')

