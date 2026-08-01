
def get_supported_codecs() -> list[str]:
    """
    :returns: A list of all supported codecs.
    """
    return [f for f in codecs if check_codec(f)]

