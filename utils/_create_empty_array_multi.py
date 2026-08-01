
def _create_empty_array_multi(space: Box, n: int = 1, fn=np.zeros) -> np.ndarray:
    return fn((n,) + space.shape, dtype=space.dtype)

