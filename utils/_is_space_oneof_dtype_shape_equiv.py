
def _is_space_oneof_dtype_shape_equiv(space_1: OneOf, space_2):
    return (
        isinstance(space_2, OneOf)
        and len(space_1) == len(space_2)
        and all(
            is_space_dtype_shape_equiv(space_1[i], space_2[i])
            for i in range(len(space_1))
        )
    )

