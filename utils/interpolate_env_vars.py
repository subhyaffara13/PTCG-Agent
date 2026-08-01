
def interpolate_env_vars(value: str, variables: Mapping[str, str]) -> str:
    """Replace ``${NAME}`` references in ``value`` with the matching mapping
    entry. Unknown names are left untouched so callers can detect them via
    ``find_env_var_references`` on the result if needed.
    """
    if not value:
        return value

    def _sub(match: "re.Match[str]") -> str:
        name = match.group(1)
        if name in variables:
            return variables[name]
        return match.group(0)

    return _ENV_VAR_PATTERN.sub(_sub, value)

