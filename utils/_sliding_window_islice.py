
def _sliding_window_islice(iterable, n):
    # Fast path for small, non-zero values of n.
    iterators = tee(iterable, n)
    for i, iterator in enumerate(iterators):
        next(islice(iterator, i, i), None)
    return zip(*iterators)

