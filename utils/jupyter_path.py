
def jupyter_path(*subdirs: str) -> list[str]:
    """Return a list of directories to search for data files.

    There are four sources of paths to search:

    - $JUPYTER_PATH environment variable (always highest priority)
    - user directories (e.g. ~/.local/share/jupyter)
    - environment directories (e.g. {sys.prefix}/share/jupyter)
    - system-wide paths (e.g. /usr/local/share/jupyter)

    JUPYTER_PATH environment variable has highest priority, if defined,
    and is purely additive.

    If the JUPYTER_PREFER_ENV_PATH environment variable is set, the environment-level
    directories will have priority over user-level directories.
    You can also set JUPYTER_PREFER_ENV_PATH=0 to explicitly prefer user directories.
    If Jupyter detects that you are in a virtualenv or conda environment,
    environment paths are also preferred to user paths,
    otherwise user paths are preferred to environment paths.

    If the Python site.ENABLE_USER_SITE variable is True, we also add the
    appropriate Python user site subdirectory to the user-level directories.

    Finally, system-wide directories, such as `/usr/local/share/jupyter` are searched.

    If ``*subdirs`` are given, that subdirectory will be added to each element.


    .. versionchanged:: 5.8

        On Windows, %PROGRAMDATA% will be used as a system-wide path only if
        the JUPYTER_USE_PROGRAMDATA env is set.
        By default, there is no default system-wide path on Windows and the env path
        is used instead.

    Examples:

    >>> jupyter_path()
    ['~/.local/jupyter', '/usr/local/share/jupyter']
    >>> jupyter_path('kernels')
    ['~/.local/jupyter/kernels', '/usr/local/share/jupyter/kernels']
    """

    paths: list[str] = []

    # highest priority is explicit environment variable
    if os.environ.get("JUPYTER_PATH"):
        paths.extend(p.rstrip(os.sep) for p in os.environ["JUPYTER_PATH"].split(os.pathsep))

    # Next is environment or user, depending on the JUPYTER_PREFER_ENV_PATH flag
    user = [jupyter_data_dir()]
    if site.ENABLE_USER_SITE:
        # Check if site.getuserbase() exists to be compatible with virtualenv,
        # which often does not have this method.
        userbase: str | None
        userbase = site.getuserbase() if hasattr(site, "getuserbase") else site.USER_BASE

        if userbase:
            userdir = str(Path(userbase, "share", "jupyter"))
            if userdir not in user:
                user.append(userdir)

    # Windows usually doesn't have a 'system' prefix,
    # so 'system' and 'env' are the same
    # make sure that env can still be preferred in this case
    if ENV_JUPYTER_PATH == SYSTEM_JUPYTER_PATH:
        env = ENV_JUPYTER_PATH
    else:
        env = [p for p in ENV_JUPYTER_PATH if p not in SYSTEM_JUPYTER_PATH]

    if prefer_environment_over_user():
        paths.extend(env)
        paths.extend(user)
    else:
        paths.extend(user)
        paths.extend(env)

    # finally, add system paths (can overlap with env, so avoid duplicates)
    for _path in SYSTEM_JUPYTER_PATH:
        if _path not in paths:
            paths.append(_path)

    # add subdir, if requested
    if subdirs:
        paths = [pjoin(p, *subdirs) for p in paths]
    return paths

