from typing import Any

def _create_empty_array_sequence(
    space: Sequence, n: int = 1, fn=np.zeros
) -> tuple[Any, ...]:
    if space.stack:
        return tuple(
            create_empty_array(space.feature_space, n=1, fn=fn) for _ in range(n)
        )
    else:
        return tuple(tuple() for _ in range(n))

