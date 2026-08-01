
def test_axis_nan_policy_axis_is_None(hypotest, args, kwds, n_samples,
                                      n_outputs, paired, unpacker, nan_policy,
                                      data_generator):
    # check for correct behavior when `axis=None`
    if not unpacker:
        def unpacker(res):
            return res

    # skip if nan emits unexpected RuntimeWarning in np.mean()
    # seen on mips64el, https://github.com/scipy/scipy/issues/22360
    # Only affects nan_policy "mixed-propagate" for selected hypotests
    if data_generator=="mixed" and nan_policy=="propagate":
        # only skip affected hypotests
        if hypotest.__name__ in ["iqr", "ttest_ci",
                                 "xp_mean_1samp", "xp_mean_2samp", "xp_var",
                                 "weightedtau", "weightedtau_weighted"]:
            skip_nan_unexpected_exception()
    # all_nans-propagate-ttest_ci is also affected, via scalar multiply
    if (data_generator=="all_nans" and nan_policy=="propagate"
        and hypotest.__name__=="ttest_ci"):
        skip_nan_unexpected_exception()
    # mixed-omit-xp_var is also affected, via subtract
    if (data_generator=="mixed" and nan_policy=="omit"
        and hypotest.__name__=="xp_var"):
        skip_nan_unexpected_exception()

    rng = np.random.default_rng(0)

    if data_generator == "empty":
        data = [rng.random((2, 0)) for i in range(n_samples)]
    else:
        data = [rng.random((2, 20)) for i in range(n_samples)]

    if data_generator == "mixed":
        masks = [rng.random((2, 20)) > 0.9 for i in range(n_samples)]
        for sample, mask in zip(data, masks):
            sample[mask] = np.nan
    elif data_generator == "all_nans":
        data = [sample * np.nan for sample in data]

    data_raveled = [sample.ravel() for sample in data]

    if nan_policy == 'raise' and data_generator not in {"all_finite", "empty"}:
        message = 'The input contains nan values'

        # check for correct behavior whether or not data is 1d to begin with
        with pytest.raises(ValueError, match=message):
            hypotest(*data, axis=None, nan_policy=nan_policy,
                     *args, **kwds)
        with pytest.raises(ValueError, match=message):
            hypotest(*data_raveled, axis=None, nan_policy=nan_policy,
                     *args, **kwds)

        return

    # behavior of reference implementation with 1d input, public function with 1d
    # input, and public function with Nd input and `axis=None` should be consistent.
    # This means:
    # - If the reference version raises an error or emits a warning, it's because
    #   the sample is too small, so check that the public function emits an
    #   appropriate "too small" warning
    # - Any results returned by the three versions should be the same.
    with warnings.catch_warnings():  # treat warnings as errors
        warnings.simplefilter("error")

        ea_str, eb_str, ec_str = None, None, None
        try:
            res1da = nan_policy_1d(hypotest, data_raveled, unpacker, *args,
                                   n_outputs=n_outputs, nan_policy=nan_policy,
                                   paired=paired, _no_deco=True, **kwds)
        except (RuntimeWarning, ValueError, ZeroDivisionError, UserWarning) as ea:
            res1da = None
            ea_str = str(ea)

        try:
            res1db = hypotest(*data_raveled, *args, nan_policy=nan_policy, **kwds)
        except SmallSampleWarning as eb:
            eb_str = str(eb)

        try:
            res1dc = hypotest(*data, *args, axis=None, nan_policy=nan_policy, **kwds)
        except SmallSampleWarning as ec:
            ec_str = str(ec)

    if ea_str or eb_str or ec_str:  # *if* there is some sort of error or warning
        # If the reference implemented generated an error or warning, make sure the
        # message was one of the expected "too small" messages. Note that some
        # functions don't complain at all without the decorator; that's OK, too.
        ok_msg = any([str(ea_str).startswith(msg) for msg in too_small_messages])
        assert (ea_str is None) or ok_msg

        # make sure the wrapped function emits the *intended* warning
        desired_warnings = {too_small_1d_omit, too_small_1d_not_omit}
        assert str(eb_str) in desired_warnings
        assert str(ec_str) in desired_warnings

        with warnings.catch_warnings():  # ignore warnings to get return value
            warnings.simplefilter("ignore")
            res1db = hypotest(*data_raveled, *args, nan_policy=nan_policy, **kwds)
            res1dc = hypotest(*data, *args, axis=None, nan_policy=nan_policy, **kwds)

    # Make sure any results returned by reference/public function are identical
    # and all attributes are *NumPy* scalars
    res1db, res1dc = unpacker(res1db), unpacker(res1dc)
    # changed from 1e-15 solely to appease macosx-x86_64+Accelerate
    assert_allclose(res1dc, res1db, rtol=2e-14)
    all_results = list(res1db) + list(res1dc)

    if res1da is not None:
        # changed from 1e-15 solely to appease macosx-x86_64+Accelerate
        assert_allclose(res1db, res1da, rtol=2e-14)
        all_results += list(res1da)

    for item in all_results:
        assert np.issubdtype(item.dtype, np.number)
        assert np.isscalar(item)

