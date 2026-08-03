from typing import Tuple

def _create_tuple_zero_array(space: Tuple):
    return tuple(create_zero_array(subspace) for subspace in space.spaces)

