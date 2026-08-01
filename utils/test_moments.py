
def test_moments(distname, arg, normalization_ok, higher_ok, moment_ok,
                 is_xfailing):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'rv_histogram_instance'

    with warnings.catch_warnings():
        warnings.filterwarnings(
            "ignore",
            "The integral is probably divergent, or slowly convergent.",
            IntegrationWarning,
        )
        warnings.filterwarnings(
            "ignore",
            "The maximum number of subdivisions.",
            IntegrationWarning
        )
        warnings.filterwarnings(
            "ignore",
            "The algorithm does not converge.",
            IntegrationWarning
        )

        if is_xfailing:
            warnings.simplefilter("ignore", IntegrationWarning)

        m, v, s, k = distfn.stats(*arg, moments='mvsk')

        with np.errstate(all="ignore"):
            if normalization_ok:
                check_normalization(distfn, arg, distname)

            if higher_ok:
                check_mean_expect(distfn, arg, m, distname)
                check_skew_expect(distfn, arg, m, v, s, distname)
                check_var_expect(distfn, arg, m, v, distname)
                check_kurt_expect(distfn, arg, m, v, k, distname)
                check_munp_expect(distfn, arg, distname)

        check_loc_scale(distfn, arg, m, v, distname)

        if moment_ok:
            check_moment(distfn, arg, m, v, distname)


def test_moments(distname, arg):
    try:
        distfn = getattr(stats, distname)
    except TypeError:
        distfn = distname
        distname = 'sample distribution'
    m, v, s, k = distfn.stats(*arg, moments='mvsk')
    check_normalization(distfn, arg, distname)

    # compare `stats` and `moment` methods
    check_moment(distfn, arg, m, v, distname)
    check_mean_expect(distfn, arg, m, distname)
    check_var_expect(distfn, arg, m, v, distname)
    check_skew_expect(distfn, arg, m, v, s, distname)
    with warnings.catch_warnings():
        if distname in ['zipf', 'betanbinom']:
            warnings.simplefilter("ignore", RuntimeWarning)
        check_kurt_expect(distfn, arg, m, v, k, distname)

    # frozen distr moments
    check_moment_frozen(distfn, arg, m, 1)
    check_moment_frozen(distfn, arg, v+m*m, 2)

