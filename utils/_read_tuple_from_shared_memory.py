from typing import Tuple

def _read_tuple_from_shared_memory(space: Tuple, shared_memory, n: int = 1):
    return tuple(
        read_from_shared_memory(subspace, memory, n=n)
        for (memory, subspace) in zip(shared_memory, space.spaces)
    )


def _read_tuple_from_shared_memory(space, shared_memory, n: int = 1):
    return tuple(
        read_from_shared_memory(subspace, memory, n=n)
        for (memory, subspace) in zip(shared_memory, space.spaces)
    )

