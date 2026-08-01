
def _ecdf_uncensored(sample):
    sample = np.sort(sample)
    x, counts = np.unique(sample, return_counts=True)

    # [1].81 "the fraction of [observations] that are less than or equal to x
    events = np.cumsum(counts)
    n = sample.size
    cdf = events / n

    # [1].89 "the relative frequency of the sample that exceeds x in value"
    sf = 1 - cdf

    at_risk = np.concatenate(([n], n - events[:-1]))
    return x, cdf, sf, at_risk, counts

