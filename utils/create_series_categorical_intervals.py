
def create_series_categorical_intervals(left, right, closed="right"):
    return Series(Categorical(IntervalIndex.from_arrays(left, right, closed)))

