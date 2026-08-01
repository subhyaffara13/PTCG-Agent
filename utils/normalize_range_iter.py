
def normalize_range_iter(range_iter: Any) -> tuple[int, int, int]:
    _, (range_obj,), maybe_idx = range_iter.__reduce__()
    # In 3.12+, `maybe_idx` could be None, and `range_obj.start` would've been
    # already incremented by the current index.
    # The index (maybe_idx) is the number of steps taken so far. To get the
    # correct start value, one must add (maybe_idx * step) to the original
    # start. See:
    # https://github.com/python/cpython/blob/ea77feecbba389916af8f90b2fc77f07910a2963/Objects/rangeobject.c#L885-L899
    start = range_obj.start + (maybe_idx or 0) * range_obj.step
    stop = range_obj.stop
    step = range_obj.step
    return (start, stop, step)

