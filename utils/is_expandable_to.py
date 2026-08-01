
def is_expandable_to(shape: ShapeType, desired: ShapeType) -> bool:
    """Checks if a shape can be expanded to another shape.
    This is equivalent to checking if the two shapes are broadcastable.
    """
    # This is a Python implementation of
    # aten/src/ATen/ExpandUtils.h:is_expandable_to
    if len(shape) > len(desired):
        return False
    for i in range(len(shape)):
        if shape[-i - 1] != desired[-i - 1] and shape[-i - 1] != 1:
            return False
    return True

