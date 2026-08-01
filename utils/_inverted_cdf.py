
def _inverted_cdf(n, quantiles):
    gamma_fun = lambda gamma, _: (gamma == 0)
    return _discrete_interpolation_to_boundaries((n * quantiles) - 1,
                                                 gamma_fun)

