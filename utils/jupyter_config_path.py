
def jupyter_config_path() -> list[str]:
    """Return the search path for Jupyter config files as a list.

    If the JUPYTER_PREFER_ENV_PATH environment variable is set, the
    environment-level directories will have priority over user-level
    directories.

    If the Python site.ENABLE_USER_SITE variable is True, we also add the
    appropriate Python user site subdirectory to the user-level directories.

    Finally, system-wide directories such as `/usr/local/etc/jupyter` are searched.


    .. versionchanged:: 5.8

        On Windows, %PROGRAMDATA% will be used as a system-wide path only if
        the JUPYTER_USE_PROGRAMDATA env is set.
        By default, there is no system-wide config path on Windows.

    Examples:

    >>> jupyter_config_path()
    ['~/.jupyter', '~/.local/etc/jupyter', '/usr/local/etc/jupyter', '/etc/jupyter']

    """
    if os.environ.get("JUPYTER_NO_CONFIG"):
        # jupyter_config_dir makes a blank config when JUPYTER_NO_CONFIG is set.
        return [jupyter_config_dir()]

    paths: list[str] = []

    # highest priority is explicit environment variable
    if os.environ.get("JUPYTER_CONFIG_PATH"):
        paths.extend(p.rstrip(os.sep) for p in os.environ["JUPYTER_CONFIG_PATH"].split(os.pathsep))

    # Next is environment or user, depending on the JUPYTER_PREFER_ENV_PATH flag
    user = [jupyter_config_dir()]
    if site.ENABLE_USER_SITE:
        userbase: str | None
        # Check if site.getuserbase() exists to be compatible with virtualenv,
        # which often does not have this method.
        userbase = site.getuserbase() if hasattr(site, "getuserbase") else site.USER_BASE

        if userbase:
            userdir = str(Path(userbase, "etc", "jupyter"))
            if userdir not in user:
                user.append(userdir)

    # Windows usually doesn't have a 'system' prefix,
    # so 'system' and 'env' are the same
    # make sure that env can still be preferred in this case
    if ENV_CONFIG_PATH == SYSTEM_CONFIG_PATH:
        env = ENV_CONFIG_PATH
    else:
        env = [p for p in ENV_CONFIG_PATH if p not in SYSTEM_CONFIG_PATH]

    if prefer_environment_over_user():
        paths.extend(env)
        paths.extend(user)
    else:
        paths.extend(user)
        paths.extend(env)

    # Finally, system path
    if ENV_CONFIG_PATH != SYSTEM_CONFIG_PATH:
        paths.extend(SYSTEM_CONFIG_PATH)
    return paths

