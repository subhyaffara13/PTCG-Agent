
def _parse_optim_args(optim_args_str: str | None) -> dict[str, str]:
    """Parse optimizer arguments from a comma-separated string."""
    if not optim_args_str:
        return {}
    optim_args = {}
    for mapping in optim_args_str.replace(" ", "").split(","):
        key, value = mapping.split("=")
        optim_args[key] = value
    return optim_args

