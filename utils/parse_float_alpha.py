
def parse_float_alpha(value: Union[None, str, float, int]) -> Optional[float]:
    """Parse an alpha value checking it's a valid float in the range 0 to 1.

    Args:
        value: The input value to parse.

    Returns:
        The parsed value as a float, or `None` if the value was None or equal 1.

    Raises:
        PydanticCustomError: If the input value cannot be successfully parsed as a float in the expected range.
    """
    if value is None:
        return None
    try:
        if isinstance(value, str) and value.endswith('%'):
            alpha = float(value[:-1]) / 100
        else:
            alpha = float(value)
    except ValueError:
        raise PydanticCustomError('color_error', 'value is not a valid color: alpha values must be a valid float')

    if math.isclose(alpha, 1):
        return None
    elif 0 <= alpha <= 1:
        return alpha
    else:
        raise PydanticCustomError('color_error', 'value is not a valid color: alpha values must be in the range 0 to 1')


def parse_float_alpha(value: Union[None, str, float, int]) -> Optional[float]:
    """
    Parse a value checking it's a valid float in the range 0 to 1
    """
    if value is None:
        return None
    try:
        if isinstance(value, str) and value.endswith('%'):
            alpha = float(value[:-1]) / 100
        else:
            alpha = float(value)
    except ValueError:
        raise ColorError(reason='alpha values must be a valid float')

    if almost_equal_floats(alpha, 1):
        return None
    elif 0 <= alpha <= 1:
        return alpha
    else:
        raise ColorError(reason='alpha values must be in the range 0 to 1')

