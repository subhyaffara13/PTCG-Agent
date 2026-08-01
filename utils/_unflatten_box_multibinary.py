
def _unflatten_box_multibinary(
    space: Box | MultiBinary, x: NDArray[Any]
) -> NDArray[Any]:
    return np.asarray(x, dtype=space.dtype).reshape(space.shape)


def _unflatten_box_multibinary(
    space: Union[Box, MultiBinary], x: np.ndarray
) -> np.ndarray:
    return np.asarray(x, dtype=space.dtype).reshape(space.shape)

