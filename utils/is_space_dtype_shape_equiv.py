
def is_space_dtype_shape_equiv(space_1: Space, space_2: Space) -> bool:
    """Returns if two spaces share a common dtype and shape (plus any critical variables).

    This function is primarily used to check for compatibility of different spaces in a vector environment.

    Args:
        space_1: A Gymnasium space
        space_2: A Gymnasium space

    Returns:
        If the two spaces share a common dtype and shape (plus any critical variables).
    """
    if isinstance(space_1, Space) and isinstance(space_2, Space):
        raise NotImplementedError(
            "`check_dtype_shape_equivalence` doesn't support Generic Gymnasium Spaces, "
        )
    else:
        raise TypeError()

