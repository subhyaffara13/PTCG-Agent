
def assert_invalid_addsub_type(left, right, msg=None):
    """
    Helper function to assert that two objects can
    neither be added nor subtracted.

    Parameters
    ----------
    left : object
        The first operand.
    right : object
        The second operand.
    msg : str or None, default None
        The error message expected in the TypeError.
    """
    with pytest.raises(TypeError, match=msg):
        left + right
    with pytest.raises(TypeError, match=msg):
        right + left
    with pytest.raises(TypeError, match=msg):
        left - right
    with pytest.raises(TypeError, match=msg):
        right - left

