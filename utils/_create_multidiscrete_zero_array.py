
def _create_multidiscrete_zero_array(space: MultiDiscrete):
    return np.array(space.start, copy=True, dtype=space.dtype)

