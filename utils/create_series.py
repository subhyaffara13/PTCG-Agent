
def create_series():
    return [
        Series(dtype=np.float64, name="a"),
        Series([np.nan] * 5),
        Series([1.0] * 5),
        Series(range(5, 0, -1)),
        Series(range(5)),
        Series([np.nan, 1.0, np.nan, 1.0, 1.0]),
        Series([np.nan, 1.0, np.nan, 2.0, 3.0]),
        Series([np.nan, 1.0, np.nan, 3.0, 2.0]),
    ]

