
def test_axis_nan_policy_decorated_pickled(hypotest, args, kwds, n_samples,
                                           n_outputs, paired, unpacker):
    if "ttest_ci" in hypotest.__name__:
        pytest.skip("Can't pickle functions defined within functions.")

    rng = np.random.default_rng(0)

    # Some hypothesis tests return a non-iterable that needs an `unpacker` to
    # extract the statistic and p-value. For those that don't:
    if not unpacker:
        def unpacker(res):
            return res

    data = rng.uniform(size=(n_samples, 2, 30))
    pickled_hypotest = pickle.dumps(hypotest)
    unpickled_hypotest = pickle.loads(pickled_hypotest)
    res1 = unpacker(hypotest(*data, *args, axis=-1, **kwds))
    res2 = unpacker(unpickled_hypotest(*data, *args, axis=-1, **kwds))
    assert_allclose(res1, res2, rtol=1e-12)

