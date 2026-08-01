
def test_ttest_ci_iv(test_fun, args, xp):
    # test `confidence_interval` method input validation
    res = test_fun(*(xp.asarray(arg) for arg in args))
    message = '`confidence_level` must be a number between 0 and 1.'
    with pytest.raises(ValueError, match=message):
        res.confidence_interval(confidence_level=10)

