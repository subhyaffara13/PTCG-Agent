
def _unflatten_multidiscrete(
    space: MultiDiscrete, x: NDArray[np.integer[Any]]
) -> NDArray[np.integer[Any]]:
    offsets = np.zeros((space.nvec.size + 1,), dtype=space.dtype)
    offsets[1:] = np.cumsum(space.nvec.flatten())
    (indices,) = np.nonzero(x)
    if len(indices) == 0:
        raise ValueError(
            f"{x} is not a concatenation of one-hot encoded vectors and can not be unflattened to space {space}. "
            "Not all valid samples in a flattened space can be unflattened."
        )
    return (
        np.asarray(indices - offsets[:-1], dtype=space.dtype).reshape(space.shape)
        + space.start
    )


def _unflatten_multidiscrete(space: MultiDiscrete, x: np.ndarray) -> np.ndarray:
    offsets = np.zeros((space.nvec.size + 1,), dtype=space.dtype)
    offsets[1:] = np.cumsum(space.nvec.flatten())

    (indices,) = cast(type(offsets[:-1]), np.nonzero(x))
    return np.asarray(indices - offsets[:-1], dtype=space.dtype).reshape(space.shape)

