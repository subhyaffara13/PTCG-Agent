
def _batch_differing_spaces_discrete(spaces: list[Discrete]):
    return MultiDiscrete(
        nvec=np.array([space.n for space in spaces]),
        start=np.array([space.start for space in spaces]),
        seed=deepcopy(spaces[0].np_random),
    )

