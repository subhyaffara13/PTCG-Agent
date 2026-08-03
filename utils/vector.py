from typing import List, Optional

def vector(
    *shape,
    element_type: Type = None,
    scalable: Optional[List[bool]] = None,
    scalable_dims: Optional[List[int]] = None,
):
    return _shaped(
        *shape,
        element_type=element_type,
        type_constructor=partial(
            VectorType.get, scalable=scalable, scalable_dims=scalable_dims
        ),
    )

