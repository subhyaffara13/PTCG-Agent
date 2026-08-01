
def test_tukeylambda_stats_mpmath():
    """Compare results with some values that were computed using mpmath."""
    a10 = dict(atol=1e-10, rtol=0)
    a12 = dict(atol=1e-12, rtol=0)
    data = [
        # lambda        variance              kurtosis
        [-0.1, 4.78050217874253547, 3.78559520346454510],
        [-0.0649, 4.16428023599895777, 2.52019675947435718],
        [-0.05, 3.93672267890775277, 2.13129793057777277],
        [-0.001, 3.30128380390964882, 1.21452460083542988],
        [0.001, 3.27850775649572176, 1.18560634779287585],
        [0.03125, 2.95927803254615800, 0.804487555161819980],
        [0.05, 2.78281053405464501, 0.611604043886644327],
        [0.0649, 2.65282386754100551, 0.476834119532774540],
        [1.2, 0.242153920578588346, -1.23428047169049726],
        [10.0, 0.00095237579757703597, 2.37810697355144933],
        [20.0, 0.00012195121951131043, 7.37654321002709531],
    ]

    for lam, var_expected, kurt_expected in data:
        var = tukeylambda_variance(lam)
        assert_allclose(var, var_expected, **a12)
        kurt = tukeylambda_kurtosis(lam)
        assert_allclose(kurt, kurt_expected, **a10)

    # Test with vector arguments (most of the other tests are for single
    # values).
    lam, var_expected, kurt_expected = zip(*data)
    var = tukeylambda_variance(lam)
    assert_allclose(var, var_expected, **a12)
    kurt = tukeylambda_kurtosis(lam)
    assert_allclose(kurt, kurt_expected, **a10)

