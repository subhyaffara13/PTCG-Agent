
def _flatten_discrete(space: Discrete, x: np.int64) -> NDArray[np.int64]:
    onehot = np.zeros(space.n, dtype=space.dtype)
    onehot[x - space.start] = 1
    return onehot


def _flatten_discrete(space, x) -> np.ndarray:
    onehot = np.zeros(space.n, dtype=space.dtype)
    onehot[x - space.start] = 1
    return onehot

