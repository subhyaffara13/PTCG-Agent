
def _flatten_space_binary(space: Discrete | MultiBinary | MultiDiscrete) -> Box:
    return Box(low=0, high=1, shape=(flatdim(space),), dtype=space.dtype)


def _flatten_space_binary(space: Union[Discrete, MultiBinary, MultiDiscrete]) -> Box:
    return Box(low=0, high=1, shape=(flatdim(space),), dtype=space.dtype)

