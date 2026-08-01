
def create_series_intervals(left, right, closed="right"):
    return Series(IntervalArray.from_arrays(left, right, closed))

