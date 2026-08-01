
def _concatenate_dict(
    space: Dict, items: Iterable, out: dict[str, Any]
) -> dict[str, Any]:
    return {
        key: concatenate(subspace, [item[key] for item in items], out[key])
        for key, subspace in space.items()
    }


def _concatenate_dict(space, items, out):
    return OrderedDict(
        [
            (key, concatenate(subspace, [item[key] for item in items], out[key]))
            for (key, subspace) in space.spaces.items()
        ]
    )

