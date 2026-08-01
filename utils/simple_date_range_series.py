
def simple_date_range_series():
    """
    Series with date range index and random data for test purposes.
    """

    def _simple_date_range_series(start, end, freq="D"):
        rng = date_range(start, end, freq=freq)
        return Series(np.random.default_rng(2).standard_normal(len(rng)), index=rng)

    return _simple_date_range_series

