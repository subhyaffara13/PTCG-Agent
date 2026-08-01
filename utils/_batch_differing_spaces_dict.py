
def _batch_differing_spaces_dict(spaces: list[Dict]):
    assert all(spaces[0].keys() == space.keys() for space in spaces)

    return Dict(
        {
            key: batch_differing_spaces([space[key] for space in spaces])
            for key in spaces[0].keys()
        },
        seed=deepcopy(spaces[0].np_random),
    )

