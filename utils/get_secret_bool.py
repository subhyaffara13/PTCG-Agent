from typing import Optional

def get_secret_bool(
    secret_name: str,
    default_value: Optional[bool] = None,
) -> Optional[bool]:
    """
    Guarantees response from 'get_secret' is either boolean or none. Used for fixing linting errors.

    Args:
        secret_name: The name of the secret to get.
        default_value: The default value to return if the secret is not found.

    Returns:
        The secret value as a boolean or None if the secret is not found.
    """
    _secret_value = get_secret(secret_name, default_value)
    if _secret_value is None:
        return None
    elif isinstance(_secret_value, bool):
        return _secret_value
    else:
        return str_to_bool(_secret_value)

