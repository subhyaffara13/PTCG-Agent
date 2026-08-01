
def test_cont_basic(distname, arg, sn, num_parallel_threads):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'

    rng = np.random.default_rng(7654565)
    rvs = distfn.rvs(size=sn, *arg, random_state=rng)
    m, v = distfn.stats(*arg)

    if distname not in {'laplace_asymmetric'}:
        # TODO: multiple checks in this function are not robust, tweaking the
        # seed above will make different distributions fail.
        check_sample_meanvar_(m, v, rvs, rng)
    check_cdf_ppf(distfn, arg, distname)
    check_sf_isf(distfn, arg, distname)
    check_cdf_sf(distfn, arg, distname)
    check_ppf_isf(distfn, arg, distname)
    check_pdf(distfn, arg, distname)
    check_pdf_logpdf(distfn, arg, distname)
    check_pdf_logpdf_at_endpoints(distfn, arg, distname)
    check_cdf_logcdf(distfn, arg, distname)
    check_sf_logsf(distfn, arg, distname)
    check_ppf_broadcast(distfn, arg, distname)

    alpha = 0.01
    if distname == 'rv_histogram_instance':
        check_distribution_rvs(distfn.cdf, arg, alpha, rvs)
    elif distname != 'geninvgauss':
        # skip kstest for geninvgauss since cdf is too slow; see test for
        # rv generation in TestGenInvGauss in test_distributions.py
        check_distribution_rvs(distname, arg, alpha, rvs)

    locscale_defaults = (0, 1)
    meths = [distfn.pdf, distfn.logpdf, distfn.cdf, distfn.logcdf,
             distfn.logsf]
    # make sure arguments are within support
    spec_x = {'weibull_max': -0.5, 'levy_l': -0.5,
              'pareto': 1.5, 'truncpareto': 3.2, 'tukeylambda': 0.3,
              'rv_histogram_instance': 5.0}
    x = spec_x.get(distname, 0.5)
    if distname == 'invweibull':
        arg = (1,)
    elif distname == 'ksone':
        arg = (3,)

    check_named_args(distfn, x, arg, locscale_defaults, meths)
    if num_parallel_threads == 1:
        check_random_state_property(distfn, arg)

        if distname in ['rel_breitwigner'] and _IS_32BIT:
            # gh18414
            pytest.skip("fails on Linux 32-bit")
        else:
            check_pickling(distfn, arg)
    check_freezing(distfn, arg)

    # Entropy
    if distname not in ['kstwobign', 'kstwo', 'ncf']:
        check_entropy(distfn, arg, distname)

    if distfn.numargs == 0:
        check_vecentropy(distfn, arg)

    if (distfn.__class__._entropy != stats.rv_continuous._entropy
            and distname != 'vonmises'):
        check_private_entropy(distfn, arg, stats.rv_continuous)

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore", "The occurrence of roundoff error", IntegrationWarning)
        warnings.filterwarnings("ignore", "Extremely bad integrand", IntegrationWarning)
        warnings.filterwarnings("ignore", "invalid value", RuntimeWarning)
        check_entropy_vect_scale(distfn, arg)

    check_retrieving_support(distfn, arg)
    check_edge_support(distfn, arg)

    check_meth_dtype(distfn, arg, meths)
    check_ppf_dtype(distfn, arg)

    # complex special functions known to fail on sparc64 (gh-22577)
    if distname not in fails_cmplx and platform.machine() != 'sparc64':
        check_cmplx_deriv(distfn, arg)

    if distname != 'truncnorm':
        check_ppf_private(distfn, arg, distname)

