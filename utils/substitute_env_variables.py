
def substitute_env_variables(value: str) -> str:
    """
    Replace {{environment_variables.VAR_NAME}} patterns with actual environment variable values

    Args:
        value: String that may contain {{environment_variables.VAR_NAME}} patterns

    Returns:
        str: String with environment variables substituted
    """
    pattern = r"\{\{environment_variables\.([A-Z_]+)\}\}"

    def replace_env_var(match):
        env_var_name = match.group(1)
        return os.getenv(env_var_name, "")

    return re.sub(pattern, replace_env_var, value)

