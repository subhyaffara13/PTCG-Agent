
def monotonic_index(start, end, dtype="int64", closed="right"):
    return IntervalIndex.from_breaks(np.arange(start, end, dtype=dtype), closed=closed)

