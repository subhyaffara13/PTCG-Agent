from typing import Tuple

def _create_tuple_shared_memory(space: Tuple, n: int = 1, ctx=mp):
    return tuple(
        create_shared_memory(subspace, n=n, ctx=ctx) for subspace in space.spaces
    )


def _create_tuple_shared_memory(space, n: int = 1, ctx=mp):
    return tuple(
        create_shared_memory(subspace, n=n, ctx=ctx) for subspace in space.spaces
    )

