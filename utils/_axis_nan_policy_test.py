
def _axis_nan_policy_test(hypotest, args, kwds, n_samples, n_outputs, paired,
                          unpacker, nan_policy, axis, data_generator):
    # Tests the 1D and vectorized behavior of hypothesis tests against a
    # reference implementation (nan_policy_1d with np.ndenumerate)

    # Some hypothesis tests return a non-iterable that needs an `unpacker` to
    # extract the statistic and p-value. For those that don't:
    if not unpacker:
        def unpacker(res):
            return res

    rng = np.random.default_rng(0)

    # Generate multi-dimensional test data with all important combinations
    # of patterns of nans along `axis`
    n_repetitions = 3  # number of repetitions of each pattern
    data_gen_kwds = {'n_samples': n_samples, 'n_repetitions': n_repetitions,
                     'axis': axis, 'rng': rng, 'paired': paired}
    if data_generator == 'mixed':
        inherent_size = 6  # number of distinct types of patterns
        data = _mixed_data_generator(**data_gen_kwds)
    elif data_generator == 'all_nans':
        inherent_size = 2  # hard-coded in _homogeneous_data_generator
        data_gen_kwds['all_nans'] = True
        data = _homogeneous_data_generator(**data_gen_kwds)
    elif data_generator == 'all_finite':
        inherent_size = 2  # hard-coded in _homogeneous_data_generator
        data_gen_kwds['all_nans'] = False
        data = _homogeneous_data_generator(**data_gen_kwds)

    output_shape = [n_repetitions] + [inherent_size]*n_samples

    # To generate reference behavior to compare against, loop over the axis-
    # slices in data. Make indexing easier by moving `axis` to the end and
    # broadcasting all samples to the same shape.
    data_b = [np.moveaxis(sample, axis, -1) for sample in data]
    data_b = [np.broadcast_to(sample, output_shape + [sample.shape[-1]])
              for sample in data_b]
    res_1d = np.zeros(output_shape + [n_outputs])

    for i, _ in np.ndenumerate(np.zeros(output_shape)):
        data1d = [sample[i] for sample in data_b]
        contains_nan = any([np.isnan(sample).any() for sample in data1d])

        # Take care of `nan_policy='raise'`.
        # Afterward, the 1D part of the test is over
        message = "The input contains nan values"
        if nan_policy == 'raise' and contains_nan:
            with pytest.raises(ValueError, match=message):
                nan_policy_1d(hypotest, data1d, unpacker, *args,
                              n_outputs=n_outputs,
                              nan_policy=nan_policy,
                              paired=paired, _no_deco=True, **kwds)

            with pytest.raises(ValueError, match=message):
                hypotest(*data1d, *args, nan_policy=nan_policy, **kwds)

            continue

        # Take care of `nan_policy='propagate'` and `nan_policy='omit'`

        # Get results of simple reference implementation
        try:
            res_1da = nan_policy_1d(hypotest, data1d, unpacker, *args,
                                    n_outputs=n_outputs,
                                    nan_policy=nan_policy,
                                    paired=paired, _no_deco=True, **kwds)
        except (ValueError, RuntimeWarning, ZeroDivisionError, UserWarning) as ea:
            ea_str = str(ea)
            if any([str(ea_str).startswith(msg) for msg in too_small_messages]):
                res_1da = np.full(n_outputs, np.nan)
            else:
                raise

        # Get results of public function with 1D slices
        # Should warn for all slices
        if (nan_policy == 'omit' and data_generator == "all_nans"
              and hypotest not in too_small_special_case_funcs):
            with pytest.warns(SmallSampleWarning, match=too_small_1d_omit):
                res = hypotest(*data1d, *args, nan_policy=nan_policy, **kwds)
        # warning depends on slice
        elif (nan_policy == 'omit' and data_generator == "mixed"
              and hypotest not in too_small_special_case_funcs):
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", too_small_1d_omit, SmallSampleWarning)
                res = hypotest(*data1d, *args, nan_policy=nan_policy, **kwds)
        # shouldn't complain if there are no NaNs
        else:
            res = hypotest(*data1d, *args, nan_policy=nan_policy, **kwds)
        res_1db = unpacker(res)

        assert_allclose(res_1db, res_1da, rtol=RTOL)
        res_1d[i] = res_1db

    res_1d = np.moveaxis(res_1d, -1, 0)

    # Perform a vectorized call to the hypothesis test.

    # If `nan_policy == 'raise'`, check that it raises the appropriate error.
    # Test is done, so return
    if nan_policy == 'raise' and not data_generator == "all_finite":
        message = 'The input contains nan values'
        with pytest.raises(ValueError, match=message):
            hypotest(*data, axis=axis, nan_policy=nan_policy, *args, **kwds)
        return

    # If `nan_policy == 'omit', we might be left with a small sample.
    # Check for the appropriate warning.
    if (nan_policy == 'omit' and data_generator in {"all_nans", "mixed"}
          and hypotest not in too_small_special_case_funcs):
        with pytest.warns(SmallSampleWarning, match=too_small_nd_omit):
            res = hypotest(*data, axis=axis, nan_policy=nan_policy, *args, **kwds)
    else:  # otherwise, there should be no warning
        res = hypotest(*data, axis=axis, nan_policy=nan_policy, *args, **kwds)

    # Compare against the output against looping over 1D slices
    res_nd = unpacker(res)

    rtol = max(tolerance_overrides.get(hypotest, RTOL), RTOL)
    assert_allclose(res_nd, res_1d, rtol=rtol)

