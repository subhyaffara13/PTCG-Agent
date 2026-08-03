from typing import Any

def _flatten_box_multibinary(space: Box | MultiBinary, x: NDArray[Any]) -> NDArray[Any]:
    return np.asarray(x, dtype=space.dtype).flatten()


def _flatten_box_multibinary(space, x) -> np.ndarray:
    return np.asarray(x, dtype=space.dtype).flatten()

