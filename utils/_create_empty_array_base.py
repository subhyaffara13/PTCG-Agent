
def _create_empty_array_base(space, n=1, fn=np.zeros):
    shape = space.shape if (n is None) else (n,) + space.shape
    return fn(shape, dtype=space.dtype)

