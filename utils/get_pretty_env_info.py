
def get_pretty_env_info():
    """
    Returns a pretty string of environment information.

    This function retrieves environment information by calling the `get_env_info` function
    and then formats the information into a human-readable string. The retrieved environment
    information is listed in the document of `get_env_info`.
    This function is used in `python collect_env.py` that should be executed when reporting a bug.

    Returns:
        str: A pretty string of the environment information.
    """
    return pretty_str(get_env_info())

