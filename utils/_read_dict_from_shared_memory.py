
def _read_dict_from_shared_memory(space: Dict, shared_memory, n: int = 1):
    return {
        key: read_from_shared_memory(subspace, shared_memory[key], n=n)
        for (key, subspace) in space.spaces.items()
    }


def _read_dict_from_shared_memory(space, shared_memory, n: int = 1):
    return OrderedDict(
        [
            (key, read_from_shared_memory(subspace, shared_memory[key], n=n))
            for (key, subspace) in space.spaces.items()
        ]
    )

