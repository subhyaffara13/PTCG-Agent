
def verify_number_and_cast(x: SupportsFloat) -> float:
    """Verify parameter is a single number and cast to a float."""
    try:
        x = float(x)
    except (ValueError, TypeError) as e:
        raise ValueError(f"An option ({x}) could not be converted to a float.") from e
    return x


def verify_number_and_cast(x: SupportsFloat) -> float:
    """Verify parameter is a single number and cast to a float."""
    try:
        x = float(x)
    except (ValueError, TypeError):
        raise ValueError(f"An option ({x}) could not be converted to a float.")
    return x

