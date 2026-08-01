
def _is_space_tuple_dtype_shape_equiv(space_1, space_2):
    return isinstance(space_2, Tuple) and all(
        is_space_dtype_shape_equiv(space_1[i], space_2[i]) for i in range(len(space_1))
    )

