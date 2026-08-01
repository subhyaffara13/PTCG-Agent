
def test_axis_nan_policy_decorated_positional_axis(axis):
    # Test for correct behavior of function decorated with
    # _axis_nan_policy_decorator whether `axis` is provided as positional or
    # keyword argument

    shape = (8, 9, 10)
    rng = np.random.default_rng(0)
    x = rng.random(shape)
    y = rng.random(shape)
    res1 = stats.mannwhitneyu(x, y, True, 'two-sided', axis)
    res2 = stats.mannwhitneyu(x, y, True, 'two-sided', axis=axis)
    assert_equal(res1, res2)

    message = "mannwhitneyu() got multiple values for argument 'axis'"
    with pytest.raises(TypeError, match=re.escape(message)):
        stats.mannwhitneyu(x, y, True, 'two-sided', axis, axis=axis)

