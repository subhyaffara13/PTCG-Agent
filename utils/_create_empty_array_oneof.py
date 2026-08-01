
def _create_empty_array_oneof(space: OneOf, n: int = 1, fn=np.zeros):
    return tuple(tuple() for _ in range(n))

