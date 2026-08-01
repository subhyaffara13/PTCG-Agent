
def test_axis_nan_policy_fast(hypotest, args, kwds, n_samples, n_outputs,
                              paired, unpacker, nan_policy, axis,
                              data_generator):
    if hypotest in {stats.kruskal} and not SCIPY_XSLOW:
        pytest.skip("Too slow.")
    _axis_nan_policy_test(hypotest, args, kwds, n_samples, n_outputs, paired,
                          unpacker, nan_policy, axis, data_generator)

