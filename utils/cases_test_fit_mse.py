
def cases_test_fit_mse():
    # the first four are so slow that I'm not sure whether they would pass
    skip_basic_fit = {'levy_stable', 'studentized_range', 'ksone', 'skewnorm',
                      'irwinhall', # hangs
                      'norminvgauss',  # super slow (~1 hr) but passes
                      'kstwo',  # very slow (~25 min) but passes
                      'geninvgauss',  # quite slow (~4 minutes) but passes
                      'gausshyper', 'genhyperbolic',  # integration warnings
                      'tukeylambda',  # close, but doesn't meet tolerance
                      'vonmises',  # can have negative CDF; doesn't play nice
                      'arcsine', 'argus', 'powerlaw', 'rdist', # don't meet tolerance
                      'poisson_binom',  # vector-valued shape parameter
                      }

    # Please keep this list in alphabetical order...
    slow_basic_fit = {'alpha', 'anglit', 'betabinom', 'bradford',
                      'chi', 'chi2', 'crystalball', 'dweibull',
                      'erlang', 'exponnorm', 'exponpow', 'exponweib',
                      'fatiguelife', 'fisk', 'foldcauchy', 'foldnorm',
                      'gamma', 'genexpon', 'genextreme', 'genhalflogistic',
                      'genlogistic', 'genpareto', 'gompertz',
                      'hypergeom', 'invweibull',
                      'johnsonsu', 'kappa3', 'kstwobign',
                      'laplace_asymmetric', 'loggamma', 'loglaplace',
                      'lognorm', 'lomax',
                      'maxwell', 'nhypergeom',
                      'pareto', 'powernorm', 'randint', 'recipinvgauss',
                      'semicircular',
                      't', 'triang', 'truncexpon', 'truncpareto',
                      'uniform',
                      'wald', 'weibull_max', 'weibull_min', 'wrapcauchy',
                      'zipfian'}

    # Please keep this list in alphabetical order...
    xslow_basic_fit = {'argus', 'beta', 'betaprime', 'burr', 'burr12',
                       'dgamma', 'dpareto_lognorm', 'f', 'gengamma', 'gennorm',
                       'invgamma', 'invgauss', 'jf_skew_t',
                       'johnsonsb', 'kappa4', 'loguniform', 'mielke',
                       'nakagami', 'ncf', 'nchypergeom_fisher',
                       'nchypergeom_wallenius', 'nct', 'ncx2',
                       'pearson3', 'powerlognorm',
                       'reciprocal', 'rel_breitwigner', 'rice',
                       'trapezoid', 'truncnorm', 'truncweibull_min',
                       'vonmises_line'}

    warns_basic_fit = {'skellam'}  # can remove mark after gh-14901 is resolved

    for dist in dict(distdiscrete + distcont):
        if dist in skip_basic_fit or not isinstance(dist, str):
            reason = "Fails. Oh well."
            yield pytest.param(dist, marks=pytest.mark.skip(reason=reason))
        elif dist in slow_basic_fit:
            reason = "too slow (>= 0.25s)"
            yield pytest.param(dist, marks=pytest.mark.slow(reason=reason))
        elif dist in xslow_basic_fit:
            reason = "too slow (>= 1.0s)"
            yield pytest.param(dist, marks=pytest.mark.xslow(reason=reason))
        elif dist in warns_basic_fit:
            mark = pytest.mark.filterwarnings('ignore::RuntimeWarning')
            yield pytest.param(dist, marks=mark)
        else:
            yield dist

