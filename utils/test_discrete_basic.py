
def test_discrete_basic(distname, arg, first_case, num_parallel_threads):
    if (isinstance(distname, str) and distname.startswith('nchypergeom')
            and num_parallel_threads > 1):
        pytest.skip(reason='nchypergeom has a global random generator')

    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'sample distribution'
    rng = np.random.RandomState(9765456)
    rvs = distfn.rvs(*arg, size=2000, random_state=rng)
    supp = np.unique(rvs)
    m, v = distfn.stats(*arg)
    check_cdf_ppf(distfn, arg, supp, distname + ' cdf_ppf')

    check_pmf_cdf(distfn, arg, distname)
    check_oth(distfn, arg, supp, distname + ' oth')
    check_edge_support(distfn, arg)

    alpha = 0.01
    check_discrete_chisquare(distfn, arg, rvs, alpha,
                             distname + ' chisquare')

    if first_case:
        locscale_defaults = (0,)
        meths = [distfn.pmf, distfn.logpmf, distfn.cdf, distfn.logcdf,
                 distfn.logsf]
        # make sure arguments are within support
        # for some distributions, this needs to be overridden
        spec_k = {'randint': 11, 'hypergeom': 4, 'bernoulli': 0,
                  'nchypergeom_wallenius': 6}
        k = spec_k.get(distname, 1)
        check_named_args(distfn, k, arg, locscale_defaults, meths)
        if distname != 'sample distribution':
            check_scale_docstring(distfn)
        if num_parallel_threads == 1:
            check_random_state_property(distfn, arg)
            if distname not in {'poisson_binom'}:  # can't be pickled
                check_pickling(distfn, arg)
        check_freezing(distfn, arg)

        # Entropy
        check_entropy(distfn, arg, distname)
        if distfn.__class__._entropy != stats.rv_discrete._entropy:
            check_private_entropy(distfn, arg, stats.rv_discrete)

