
def get_random(shape, *, dtype, rng):
    A = rng.random(shape)
    if np.issubdtype(dtype, np.complexfloating):
        A = A + rng.random(shape) * 1j
    return A.astype(dtype)

