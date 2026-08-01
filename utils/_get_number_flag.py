
def _get_number_flag() -> int:
    """Register and return the NUMBER flag."""
    import doctest

    return doctest.register_optionflag("NUMBER")

