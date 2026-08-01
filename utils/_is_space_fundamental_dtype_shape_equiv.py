
def _is_space_fundamental_dtype_shape_equiv(space_1, space_2):
    return (
        # this check is necessary as singledispatch only checks the first variable and there are many options
        type(space_1) is type(space_2)
        and space_1.shape == space_2.shape
        and space_1.dtype == space_2.dtype
    )

