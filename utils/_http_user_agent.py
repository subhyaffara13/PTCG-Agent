
def _http_user_agent(
    *,
    library_name: str | None = None,
    library_version: str | None = None,
    user_agent: dict | str | None = None,
) -> str:
    """Format a user-agent string containing information about the installed packages.

    Args:
        library_name (`str`, *optional*):
            The name of the library that is making the HTTP request.
        library_version (`str`, *optional*):
            The version of the library that is making the HTTP request.
        user_agent (`str`, `dict`, *optional*):
            The user agent info in the form of a dictionary or a single string.

    Returns:
        The formatted user-agent string.
    """
    if library_name is not None:
        ua = f"{library_name}/{library_version}"
    else:
        ua = "unknown/None"
    ua += f"; hf_hub/{get_hf_hub_version()}"
    ua += f"; python/{get_python_version()}"

    if not constants.HF_HUB_DISABLE_TELEMETRY:
        if is_torch_available():
            ua += f"; torch/{get_torch_version()}"

        agent = detect_agent()
        if agent:
            ua += f"; agent/{agent}"

    if isinstance(user_agent, dict):
        ua += "; " + "; ".join(f"{k}/{v}" for k, v in user_agent.items())
    elif isinstance(user_agent, str):
        ua += "; " + user_agent

    # Retrieve user-agent origin headers from environment variable
    origin = constants.HF_HUB_USER_AGENT_ORIGIN
    if origin is not None:
        ua += "; origin/" + origin

    return _deduplicate_user_agent(ua)

