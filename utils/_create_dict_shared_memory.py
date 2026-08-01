
def _create_dict_shared_memory(space: Dict, n: int = 1, ctx=mp):
    return {
        key: create_shared_memory(subspace, n=n, ctx=ctx)
        for (key, subspace) in space.spaces.items()
    }


def _create_dict_shared_memory(space, n=1, ctx=mp):
    return OrderedDict(
        [
            (key, create_shared_memory(subspace, n=n, ctx=ctx))
            for (key, subspace) in space.spaces.items()
        ]
    )

