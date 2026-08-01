
def create_categorical_intervals(left, right, closed="right"):
    return Categorical(IntervalIndex.from_arrays(left, right, closed))

