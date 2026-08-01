
def _path_with_self() -> list[str]:
    """Put `jupyter`'s dir at the front of PATH

    Ensures that /path/to/jupyter subcommand
    will do /path/to/jupyter-subcommand
    even if /other/jupyter-subcommand is ahead of it on PATH
    """
    path_list = (os.environ.get("PATH") or os.defpath).split(os.pathsep)

    # Insert the "scripts" directory for this Python installation
    # This allows the "jupyter" command to be relocated, while still
    # finding subcommands that have been installed in the default
    # location.
    # We put the scripts directory at the *end* of PATH, so that
    # if the user explicitly overrides a subcommand, that override
    # still takes effect.
    try:
        bindir = sysconfig.get_path("scripts")
    except KeyError:
        # The Python environment does not specify a "scripts" location
        pass
    else:
        path_list.append(bindir)

    scripts = [sys.argv[0]]
    if Path(scripts[0]).is_symlink():
        # include realpath, if `jupyter` is a symlink
        scripts.append(os.path.realpath(scripts[0]))

    for script in scripts:
        bindir = str(Path(script).parent)
        if Path(bindir).is_dir() and os.access(script, os.X_OK):  # only if it's a script
            # ensure executable's dir is on PATH
            # avoids missing subcommands when jupyter is run via absolute path
            path_list.insert(0, bindir)
    return path_list

