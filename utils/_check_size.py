
def _check_size(size: Any) -> None:
    """
    Common check to enforce type and sanity check on size tuples

    :param size: Should be a 2 tuple of (width, height)
    :returns: None, or raises a ValueError
    """

    if not isinstance(size, (list, tuple)):
        msg = "Size must be a list or tuple"
        raise ValueError(msg)
    if len(size) != 2:
        msg = "Size must be a sequence of length 2"
        raise ValueError(msg)
    if size[0] < 0 or size[1] < 0:
        msg = "Width and height must be >= 0"
        raise ValueError(msg)

