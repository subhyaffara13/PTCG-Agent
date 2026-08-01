
def get_supported_features() -> list[str]:
    """
    :returns: A list of all supported features.
    """
    return [f for f in features if check_feature(f)]

