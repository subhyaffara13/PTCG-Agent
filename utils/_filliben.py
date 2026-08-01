
def _filliben(dist, data, axis):
    # [7] Section 8 # 1
    X = np.sort(data, axis=-1)

    # [7] Section 8 # 2
    n = data.shape[-1]
    k = np.arange(1, n+1)
    # Filliben used an approximation for the uniform distribution order
    # statistic medians.
    # m = (k - .3175)/(n + 0.365)
    # m[-1] = 0.5**(1/n)
    # m[0] = 1 - m[-1]
    # We can just as easily use the (theoretically) exact values. See e.g.
    # https://en.wikipedia.org/wiki/Order_statistic
    # "Order statistics sampled from a uniform distribution"
    m = stats.beta(k, n + 1 - k).median()

    # [7] Section 8 # 3
    M = dist.ppf(m)

    # [7] Section 8 # 4
    return _corr(X, M)

