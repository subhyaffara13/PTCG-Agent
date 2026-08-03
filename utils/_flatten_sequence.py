from typing import Any

def _flatten_sequence(
    space: Sequence, x: tuple[Any, ...] | Any
) -> tuple[Any, ...] | Any:
    if space.stack:
        samples_iters = gym.vector.utils.iterate(space.stacked_feature_space, x)
        flattened_samples = [
            flatten(space.feature_space, sample) for sample in samples_iters
        ]
        flattened_space = flatten_space(space.feature_space)
        out = gym.vector.utils.create_empty_array(
            flattened_space, n=len(flattened_samples)
        )
        return gym.vector.utils.concatenate(flattened_space, flattened_samples, out)
    else:
        return tuple(flatten(space.feature_space, item) for item in x)


def _flatten_sequence(space, x) -> tuple:
    return tuple(flatten(space.feature_space, item) for item in x)

