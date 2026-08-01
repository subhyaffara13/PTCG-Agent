
def _chk_asarrays(arrays, axis=None):
    arrays = [np.asanyarray(a) for a in arrays]
    if axis is None:
        # np < 1.10 ravel removes subclass from arrays
        arrays = [np.ravel(a) if a.ndim != 1 else a
                  for a in arrays]
        axis = 0
    arrays = tuple(np.atleast_1d(a) for a in arrays)
    if axis < 0:
        if not all(a.ndim == arrays[0].ndim for a in arrays):
            raise ValueError("array ndim must be the same for neg axis")
        axis = range(arrays[0].ndim)[axis]
    return arrays + (axis,)

