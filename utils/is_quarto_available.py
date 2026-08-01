
def is_quarto_available(min_version=QUARTO_MIN_VERSION):
    """Is Quarto available?"""
    try:
        raise_if_quarto_is_not_available(min_version=min_version)
        return True
    except QuartoError:
        return False

