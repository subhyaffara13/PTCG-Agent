
def _gen_param_group_key(param_keys: list[str]) -> str:
    """Concatenate all param keys as a unique identifier for one param group."""
    return "/".join(sorted(param_keys))

