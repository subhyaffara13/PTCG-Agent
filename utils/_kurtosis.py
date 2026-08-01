
def _kurtosis(data):
    """Fisher's excess kurtosis is fourth central moment / variance**2 - 3."""
    data = np.ravel(data)
    mu = data.mean()
    m2 = ((data - mu)**2).mean()
    m4 = ((data - mu)**4).mean()
    return m4 / m2**2 - 3

