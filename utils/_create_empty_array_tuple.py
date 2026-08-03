from typing import Any, Tuple

def _create_empty_array_tuple(space: Tuple, n: int = 1, fn=np.zeros) -> tuple[Any, ...]:
    return tuple(create_empty_array(subspace, n=n, fn=fn) for subspace in space.spaces)


def _create_empty_array_tuple(space, n=1, fn=np.zeros):
    return tuple(create_empty_array(subspace, n=n, fn=fn) for subspace in space.spaces)

