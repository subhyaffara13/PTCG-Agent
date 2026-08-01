
def _flatdim_tuple(space: Tuple) -> int:
    if space.is_np_flattenable:
        return sum(flatdim(s) for s in space.spaces)
    raise ValueError(
        f"{space} cannot be flattened to a numpy array, probably because it contains a `Graph` or `Sequence` subspace"
    )


def _flatdim_tuple(space: Tuple) -> int:
    if space.is_np_flattenable:
        return sum(flatdim(s) for s in space.spaces)
    raise ValueError(
        f"{space} cannot be flattened to a numpy array, probably because it contains a `Graph` or `Sequence` subspace"
    )

