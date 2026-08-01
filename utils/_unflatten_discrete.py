
def _unflatten_discrete(space: Discrete, x: NDArray[np.int64]) -> np.int64:
    nonzero = np.nonzero(x)
    if len(nonzero[0]) == 0:
        raise ValueError(
            f"{x} is not a valid one-hot encoded vector and can not be unflattened to space {space}. "
            "Not all valid samples in a flattened space can be unflattened."
        )
    return space.start + nonzero[0][0]


def _unflatten_discrete(space: Discrete, x: np.ndarray) -> int:
    return int(space.start + np.nonzero(x)[0][0])

