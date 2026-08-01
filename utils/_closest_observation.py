
def _closest_observation(n, quantiles):
    # "choose the nearest even order statistic at g=0" (H&F (1996) pp. 362).
    # Order is 1-based so for zero-based indexing round to nearest odd index.
    gamma_fun = lambda gamma, index: (gamma == 0) & (np.floor(index) % 2 == 1)
    return _discrete_interpolation_to_boundaries((n * quantiles) - 1 - 0.5,
                                                 gamma_fun)

