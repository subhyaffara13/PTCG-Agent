
def _iterate_dict(space: Dict, items: dict[str, Any]):
    keys, values = zip(
        *[
            (key, iterate(subspace, items[key]))
            for key, subspace in space.spaces.items()
        ]
    )
    for item in zip(*values):
        yield {key: value for key, value in zip(keys, item)}


def _iterate_dict(space, items):
    keys, values = zip(
        *[
            (key, iterate(subspace, items[key]))
            for key, subspace in space.spaces.items()
        ]
    )
    for item in zip(*values):
        yield OrderedDict([(key, value) for (key, value) in zip(keys, item)])

