
def assert_cannot_add(left, right, msg="cannot add"):
    """
    Helper function to assert that two objects cannot be added.

    Parameters
    ----------
    left : object
        The first operand.
    right : object
        The second operand.
    msg : str, default "cannot add"
        The error message expected in the TypeError.
    """
    with pytest.raises(TypeError, match=msg):
        left + right
    with pytest.raises(TypeError, match=msg):
        right + left

