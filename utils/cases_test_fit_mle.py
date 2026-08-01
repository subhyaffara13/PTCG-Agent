
def cases_test_fit_mle():
    # These fail default test or hang
    skip_basic_fit = {'argus', 'irwinhall', 'foldnorm', 'truncpareto',
                      'truncweibull_min', 'ksone', 'levy_stable',
                      'studentized_range', 'kstwo',
                      'beta', 'nakagami', 'truncnorm', # don't meet tolerance
                      'poisson_binom'}  # vector-valued shape parameter

    # Please keep this list in alphabetical order...
    slow_basic_fit = {'alpha', 'arcsine', 'betaprime', 'binom', 'bradford', 'burr12',
                      'chi', 'crystalball', 'dweibull', 'erlang', 'exponnorm',
                      'exponpow', 'f', 'fatiguelife', 'fisk', 'foldcauchy', 'gamma',
                      'genexpon', 'genextreme', 'gennorm', 'genpareto',
                      'gompertz', 'invgamma', 'invgauss', 'invweibull',
                      'jf_skew_t', 'johnsonsb', 'johnsonsu', 'kappa3',
                      'kstwobign', 'loglaplace', 'lognorm', 'lomax', 'mielke',
                      'nbinom', 'norminvgauss',
                      'pareto', 'pearson3', 'powerlaw', 'powernorm',
                      'randint', 'rdist', 'recipinvgauss', 'rice', 'skewnorm',
                      't', 'uniform', 'weibull_max', 'weibull_min', 'wrapcauchy',
                      'zipfian'}

    # Please keep this list in alphabetical order...
    xslow_basic_fit = {'betabinom', 'betanbinom', 'burr', 'dpareto_lognorm',
                       'exponweib', 'gausshyper', 'gengamma', 'genhalflogistic',
                       'genhyperbolic', 'geninvgauss',
                       'hypergeom', 'kappa4', 'loguniform',
                       'ncf', 'nchypergeom_fisher', 'nchypergeom_wallenius',
                       'nct', 'ncx2', 'nhypergeom',
                       'powerlognorm', 'reciprocal', 'rel_breitwigner',
                       'skellam', 'trapezoid', 'triang',
                       'tukeylambda', 'vonmises'}

    for dist in dict(distdiscrete + distcont):
        if dist in skip_basic_fit or not isinstance(dist, str):
            reason = "tested separately"
            yield pytest.param(dist, marks=pytest.mark.skip(reason=reason))
        elif dist in slow_basic_fit:
            reason = "too slow (>= 0.25s)"
            yield pytest.param(dist, marks=pytest.mark.slow(reason=reason))
        elif dist in xslow_basic_fit:
            reason = "too slow (>= 1.0s)"
            yield pytest.param(dist, marks=pytest.mark.xslow(reason=reason))
        else:
            yield dist

