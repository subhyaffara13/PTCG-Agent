
def test_genextreme_give_no_warnings():
    """regression test for gh-6219"""

    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")

        stats.genextreme.cdf(.5, 0)
        stats.genextreme.pdf(.5, 0)
        stats.genextreme.ppf(.5, 0)
        stats.genextreme.logpdf(-np.inf, 0.0)
        number_of_warnings_thrown = len(w)
        assert_equal(number_of_warnings_thrown, 0)

