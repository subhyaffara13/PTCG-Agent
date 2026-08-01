
def _is_space_sequence_dtype_shape_equiv(space_1: Sequence, space_2):
    return (
        isinstance(space_2, Sequence)
        and space_1.stack is space_2.stack
        and is_space_dtype_shape_equiv(space_1.feature_space, space_2.feature_space)
    )

