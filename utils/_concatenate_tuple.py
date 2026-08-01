
def _concatenate_tuple(
    space: Tuple, items: Iterable, out: tuple[Any, ...]
) -> tuple[Any, ...]:
    return tuple(
        concatenate(subspace, [item[i] for item in items], out[i])
        for (i, subspace) in enumerate(space.spaces)
    )


def _concatenate_tuple(space, items, out):
    return tuple(
        concatenate(subspace, [item[i] for item in items], out[i])
        for (i, subspace) in enumerate(space.spaces)
    )

