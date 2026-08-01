
def range_to_ndarray(rng: range) -> np.ndarray:
    """
    Cast a range object to ndarray.
    """
    # GH#30171 perf avoid realizing range as a list in np.array
    try:
        arr = np.arange(rng.start, rng.stop, rng.step, dtype="int64")
    except OverflowError:
        # GH#30173 handling for ranges that overflow int64
        if (rng.start >= 0 and rng.step > 0) or (rng.step < 0 <= rng.stop):
            try:
                arr = np.arange(rng.start, rng.stop, rng.step, dtype="uint64")
            except OverflowError:
                arr = construct_1d_object_array_from_listlike(list(rng))
        else:
            arr = construct_1d_object_array_from_listlike(list(rng))
    return arr

