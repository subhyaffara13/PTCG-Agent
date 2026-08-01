
def check_nans_and_edges(dist, fname, arg, res):

    valid_parameters = get_valid_parameters(dist)
    if fname in {'icdf', 'iccdf'}:
        arg_domain = _RealInterval(endpoints=(0, 1), inclusive=(True, True))
    elif fname in {'ilogcdf', 'ilogccdf'}:
        arg_domain = _RealInterval(endpoints=(-inf, 0), inclusive=(True, True))
    else:
        arg_domain = dist._variable.domain

    classified_args = classify_arg(dist, arg, arg_domain)
    valid_parameters, *classified_args = np.broadcast_arrays(valid_parameters,
                                                             *classified_args)
    valid_arg, endpoint_arg, outside_arg, nan_arg = classified_args
    all_valid = valid_arg & valid_parameters

    # Check NaN pattern and edge cases
    assert_equal(res[~valid_parameters], np.nan)
    assert_equal(res[nan_arg], np.nan)

    a, b = dist.support()
    a = np.broadcast_to(a, res.shape)
    b = np.broadcast_to(b, res.shape)

    outside_arg_minus = (outside_arg == -1) & valid_parameters
    outside_arg_plus = (outside_arg == 1) & valid_parameters
    endpoint_arg_minus = (endpoint_arg == -1) & valid_parameters
    endpoint_arg_plus = (endpoint_arg == 1) & valid_parameters

    is_discrete = isinstance(dist, DiscreteDistribution)
    # Writing this independently of how the are set in the distribution
    # infrastructure. That is very compact; this is very verbose.
    if fname in {'logpdf'}:
        assert_equal(res[outside_arg_minus], -np.inf)
        assert_equal(res[outside_arg_plus], -np.inf)
        ref = -np.inf if not is_discrete else np.inf
        assert_equal(res[endpoint_arg_minus & ~valid_arg], ref)
        assert_equal(res[endpoint_arg_plus & ~valid_arg], ref)
    elif fname in {'pdf'}:
        assert_equal(res[outside_arg_minus], 0)
        assert_equal(res[outside_arg_plus], 0)
        ref = 0 if not is_discrete else np.inf
        assert_equal(res[endpoint_arg_minus & ~valid_arg], ref)
        assert_equal(res[endpoint_arg_plus & ~valid_arg], ref)
    elif fname in {'logcdf'} and not is_discrete:
        assert_equal(res[outside_arg_minus], -inf)
        assert_equal(res[outside_arg_plus], 0)
        assert_equal(res[endpoint_arg_minus], -inf)
        assert_equal(res[endpoint_arg_plus], 0)
    elif fname in {'cdf'} and not is_discrete:
        assert_equal(res[outside_arg_minus], 0)
        assert_equal(res[outside_arg_plus], 1)
        assert_equal(res[endpoint_arg_minus], 0)
        assert_equal(res[endpoint_arg_plus], 1)
    elif fname in {'logccdf'} and not is_discrete:
        assert_equal(res[outside_arg_minus], 0)
        assert_equal(res[outside_arg_plus], -inf)
        assert_equal(res[endpoint_arg_minus], 0)
        assert_equal(res[endpoint_arg_plus], -inf)
    elif fname in {'ccdf'} and not is_discrete:
        assert_equal(res[outside_arg_minus], 1)
        assert_equal(res[outside_arg_plus], 0)
        assert_equal(res[endpoint_arg_minus], 1)
        assert_equal(res[endpoint_arg_plus], 0)
    elif fname in {'ilogcdf', 'icdf'} and not is_discrete:
        assert_equal(res[outside_arg == -1], np.nan)
        assert_equal(res[outside_arg == 1], np.nan)
        assert_equal(res[endpoint_arg == -1], a[endpoint_arg == -1])
        assert_equal(res[endpoint_arg == 1], b[endpoint_arg == 1])
    elif fname in {'ilogccdf', 'iccdf'} and not is_discrete:
        assert_equal(res[outside_arg == -1], np.nan)
        assert_equal(res[outside_arg == 1], np.nan)
        assert_equal(res[endpoint_arg == -1], b[endpoint_arg == -1])
        assert_equal(res[endpoint_arg == 1], a[endpoint_arg == 1])

    exclude = {'logmean', 'mean', 'logskewness', 'skewness', 'support'}
    if isinstance(dist, DiscreteDistribution):
        exclude.update({'pdf', 'logpdf'})

    if fname not in exclude:
        assert np.isfinite(res[all_valid & (endpoint_arg == 0)]).all()

