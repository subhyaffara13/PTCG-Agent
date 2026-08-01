
def _is_param_allowed(
    param: str,
    request_body_value: Any,
    configurable_clientside_auth_params: CONFIGURABLE_CLIENTSIDE_AUTH_PARAMS,
) -> bool:
    """
    Check if param is a str or dict and if request_body_value is in the list of allowed values
    """
    if configurable_clientside_auth_params is None:
        return False

    for item in configurable_clientside_auth_params:
        if isinstance(item, str) and param == item:
            return True
        elif isinstance(item, Dict):
            if param == "api_base" and check_regex_or_str_match(
                request_body_value=request_body_value,
                regex_str=item["api_base"],
            ):  # assume param is a regex
                return True

    return False

