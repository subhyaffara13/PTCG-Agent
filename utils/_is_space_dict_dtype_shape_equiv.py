from typing import Dict

def _is_space_dict_dtype_shape_equiv(space_1: Dict, space_2):
    return (
        isinstance(space_2, Dict)
        and space_1.keys() == space_2.keys()
        and all(
            is_space_dtype_shape_equiv(space_1[key], space_2[key])
            for key in space_1.keys()
        )
    )

