
def _kaplan_meier_reference(times, censored):
    # This is a very straightforward implementation of the Kaplan-Meier
    # estimator that does almost everything differently from the implementation
    # in stats.ecdf.

    # Begin by sorting the raw data. Note that the order of death and loss
    # at a given time matters: death happens first. See [2] page 461:
    # "These conventions may be paraphrased by saying that deaths recorded as
    # of an age t are treated as if they occurred slightly before t, and losses
    # recorded as of an age t are treated as occurring slightly after t."
    # We implement this by sorting the data first by time, then by `censored`,
    # (which is 0 when there is a death and 1 when there is only a loss).
    dtype = [('time', float), ('censored', int)]
    data = np.array([(t, d) for t, d in zip(times, censored)], dtype=dtype)
    data = np.sort(data, order=('time', 'censored'))
    times = data['time']
    died = np.logical_not(data['censored'])

    m = times.size
    n = np.arange(m, 0, -1)  # number at risk
    sf = np.cumprod((n - died) / n)

    # Find the indices of the *last* occurrence of unique times. The
    # corresponding entries of `times` and `sf` are what we want.
    _, indices = np.unique(times[::-1], return_index=True)
    ref_times = times[-indices - 1]
    ref_sf = sf[-indices - 1]
    return ref_times, ref_sf

