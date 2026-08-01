
def _batch_space_custom(space: Graph | Text | Sequence | OneOf, n: int = 1):
    # Without deepcopy, then the space.np_random is batched_space.spaces[0].np_random
    # Which is an issue if you are sampling actions of both the original space and the batched space
    batched_space = Tuple(
        tuple(deepcopy(space) for _ in range(n)), seed=deepcopy(space.np_random)
    )
    space_rng = deepcopy(space.np_random)
    new_seeds = list(map(int, space_rng.integers(0, 1e8, n)))
    batched_space.seed(new_seeds)
    return batched_space


def _batch_space_custom(space, n=1):
    # Without deepcopy, then the space.np_random is batched_space.spaces[0].np_random
    # Which is an issue if you are sampling actions of both the original space and the batched space
    batched_space = Tuple(
        tuple(deepcopy(space) for _ in range(n)), seed=deepcopy(space.np_random)
    )
    new_seeds = list(map(int, batched_space.np_random.integers(0, 1e8, n)))
    batched_space.seed(new_seeds)
    return batched_space

