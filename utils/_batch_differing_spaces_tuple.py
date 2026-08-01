
def _batch_differing_spaces_tuple(spaces: list[Tuple]):
    return Tuple(
        tuple(
            batch_differing_spaces(subspaces)
            for subspaces in zip(*[space.spaces for space in spaces])
        ),
        seed=deepcopy(spaces[0].np_random),
    )

