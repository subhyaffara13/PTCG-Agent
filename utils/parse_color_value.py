
def parse_color_value(value: Union[int, str], max_val: int = 255) -> float:
    """Parse the color value provided and return a number between 0 and 1.

    Args:
        value: An integer or string color value.
        max_val: Maximum range value. Defaults to 255.

    Raises:
        PydanticCustomError: If the value is not a valid color.

    Returns:
        A number between 0 and 1.
    """
    try:
        color = float(value)
    except ValueError:
        raise PydanticCustomError('color_error', 'value is not a valid color: color values must be a valid number')
    if 0 <= color <= max_val:
        return color / max_val
    else:
        raise PydanticCustomError(
            'color_error',
            'value is not a valid color: color values must be in the range 0 to {max_val}',
            {'max_val': max_val},
        )


def parse_color_value(value: Union[int, str], max_val: int = 255) -> float:
    """
    Parse a value checking it's a valid int in the range 0 to max_val and divide by max_val to give a number
    in the range 0 to 1
    """
    try:
        color = float(value)
    except ValueError:
        raise ColorError(reason='color values must be a valid number')
    if 0 <= color <= max_val:
        return color / max_val
    else:
        raise ColorError(reason=f'color values must be in the range 0 to {max_val}')

