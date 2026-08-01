
def test_axis_nan_policy_decorated_positional_args():
    # Test for correct behavior of function decorated with
    # _axis_nan_policy_decorator when function accepts *args

    shape = (3, 8, 9, 10)
    rng = np.random.default_rng(0)
    x = rng.random(shape)
    x[0, 0, 0, 0] = np.nan
    stats.kruskal(*x)

    message = "kruskal() got an unexpected keyword argument 'samples'"
    with pytest.raises(TypeError, match=re.escape(message)):
        stats.kruskal(samples=x)

    with pytest.raises(TypeError, match=re.escape(message)):
        stats.kruskal(*x, samples=x)

