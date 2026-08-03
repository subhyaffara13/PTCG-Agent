from typing import Set

def find_env_var_references(value: str) -> Set[str]:
    """Return the set of ``${NAME}`` identifiers referenced inside ``value``."""
    if not value:
        return set()
    return set(_ENV_VAR_PATTERN.findall(value))

