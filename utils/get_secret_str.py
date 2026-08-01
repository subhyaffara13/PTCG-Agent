
def get_secret_str(
    secret_name: str,
    default_value: Optional[Union[str, bool]] = None,
) -> Optional[str]:
    """
    Guarantees response from 'get_secret' is either string or none. Used for fixing linting errors.
    """
    value = get_secret(secret_name=secret_name, default_value=default_value)
    if value is not None and not isinstance(value, str):
        return None

    return value

