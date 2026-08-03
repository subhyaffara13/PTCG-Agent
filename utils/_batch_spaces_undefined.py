from typing import Tuple

def _batch_spaces_undefined(spaces: list[Graph | Text | Sequence | OneOf]):
    return Tuple(
        [deepcopy(space) for space in spaces], seed=deepcopy(spaces[0].np_random)
    )

