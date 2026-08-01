
def get_period_alias(offset_str: str) -> str | None:
    """
    Alias to closest period strings BQ->Q etc.
    """
    return OFFSET_TO_PERIOD_FREQSTR.get(offset_str, None)

