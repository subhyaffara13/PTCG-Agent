
def rand_series_with_duplicate_datetimeindex() -> Series:
    """
    Fixture for Series with a DatetimeIndex that has duplicates.
    """
    dates = [
        datetime(2000, 1, 2),
        datetime(2000, 1, 2),
        datetime(2000, 1, 2),
        datetime(2000, 1, 3),
        datetime(2000, 1, 3),
        datetime(2000, 1, 3),
        datetime(2000, 1, 4),
        datetime(2000, 1, 4),
        datetime(2000, 1, 4),
        datetime(2000, 1, 5),
    ]

    return Series(np.random.default_rng(2).standard_normal(len(dates)), index=dates)

