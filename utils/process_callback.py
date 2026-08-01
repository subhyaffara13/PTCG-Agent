
def process_callback(
    _callback: str, callback_type: str, environment_variables: dict
) -> dict:
    """Process a single callback and return its data with environment variables"""
    env_vars = CustomLogger.get_callback_env_vars(_callback)

    env_vars_dict: dict[str, str | None] = {}
    for _var in env_vars:
        env_variable = environment_variables.get(_var, None)
        if env_variable is None:
            env_vars_dict[_var] = None
        else:
            env_vars_dict[_var] = env_variable

    return {"name": _callback, "variables": env_vars_dict, "type": callback_type}

