
def test_axis_nan_policy_decorated_keyword_samples():
    # Test for correct behavior of function decorated with
    # _axis_nan_policy_decorator whether samples are provided as positional or
    # keyword arguments

    shape = (2, 8, 9, 10)
    rng = np.random.default_rng(0)
    x = rng.random(shape)
    x[0, 0, 0, 0] = np.nan
    res1 = stats.mannwhitneyu(*x)
    res2 = stats.mannwhitneyu(x=x[0], y=x[1])
    assert_equal(res1, res2)

    message = "mannwhitneyu() got multiple values for argument"
    with pytest.raises(TypeError, match=re.escape(message)):
        stats.mannwhitneyu(*x, x=x[0], y=x[1])

