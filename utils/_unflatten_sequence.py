from typing import Any

def _unflatten_sequence(space: Sequence, x: tuple[Any, ...]) -> tuple[Any, ...] | Any:
    if space.stack:
        flattened_space = flatten_space(space.feature_space)
        flatten_iters = gym.vector.utils.iterate(flattened_space, x)
        unflattened_samples = [
            unflatten(space.feature_space, sample) for sample in flatten_iters
        ]
        out = gym.vector.utils.create_empty_array(
            space.feature_space, len(unflattened_samples)
        )
        return gym.vector.utils.concatenate(
            space.feature_space, unflattened_samples, out
        )
    else:
        return tuple(unflatten(space.feature_space, item) for item in x)


def _unflatten_sequence(space: Sequence, x: tuple) -> tuple:
    return tuple(unflatten(space.feature_space, item) for item in x)

