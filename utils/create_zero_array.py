
def create_zero_array(space: Space[T_cov]) -> T_cov:
    """Creates a zero-based array of a space, this is similar to ``create_empty_array`` except all arrays are valid samples from the space.

    As some ``Box`` cases have ``high`` or ``low`` that don't contain zero then the ``create_empty_array`` would in case
    create arrays which is not contained in the space.

    Args:
        space: The space to create a zero array for

    Returns:
        Valid sample from the space that is as close to zero as possible
    """
    if isinstance(space, Space):
        raise CustomSpaceError(
            f"Space of type `{type(space)}` doesn't have an registered `create_zero_array` function. Register `{type(space)}` for `create_zero_array` to support it."
        )
    else:
        raise TypeError(
            f"The space provided to `create_zero_array` is not a gymnasium Space instance, type: {type(space)}, {space}"
        )

