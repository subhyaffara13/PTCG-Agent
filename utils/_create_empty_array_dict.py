
def _create_empty_array_dict(space: Dict, n: int = 1, fn=np.zeros) -> dict[str, Any]:
    return {
        key: create_empty_array(subspace, n=n, fn=fn) for key, subspace in space.items()
    }


def _create_empty_array_dict(space, n=1, fn=np.zeros):
    return OrderedDict(
        [
            (key, create_empty_array(subspace, n=n, fn=fn))
            for (key, subspace) in space.spaces.items()
        ]
    )

