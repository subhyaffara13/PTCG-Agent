
def _generate_config_filename(request_key: str) -> str:
    """
    Generate a filename for the full ops.
    """
    return f"{CONFIG_PREFIX}_{request_key}.json"

