
def _get_equivalent_key(key: str, available_keys: set) -> Optional[str]:
    """
    Get the equivalent key from available keys, checking both camelCase and snake_case variants
    """
    if key in available_keys:
        return key

    # Try camelCase version
    camel_key = _snake_to_camel(key)
    if camel_key in available_keys:
        return camel_key

    # Try snake_case version
    snake_key = _camel_to_snake(key)
    if snake_key in available_keys:
        return snake_key

    return None

