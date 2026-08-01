
def _get_default_team_param(field: str) -> Any:
    """
    Returns a default value for the given field from litellm.default_team_params config.
    Returns None if no default is configured.

    For list fields containing enums (e.g. team_member_permissions), converts enum values to strings.
    """
    default_params = litellm.default_team_params
    if default_params is None:
        return None
    if isinstance(default_params, dict):
        value = default_params.get(field)
    else:
        value = getattr(default_params, field, None)
    if value is None:
        return None
    # Convert enum values in lists to strings
    if isinstance(value, list):
        return [v.value if hasattr(v, "value") else v for v in value]
    return value

