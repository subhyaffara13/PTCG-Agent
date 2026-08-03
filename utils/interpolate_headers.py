from typing import Dict

def interpolate_headers(
    headers: Mapping[str, str], variables: Mapping[str, str]
) -> Dict[str, str]:
    """Return a copy of ``headers`` with every value passed through ``interpolate_env_vars``."""
    return {k: interpolate_env_vars(v, variables) for k, v in headers.items()}

