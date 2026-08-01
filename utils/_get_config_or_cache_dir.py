
def _get_config_or_cache_dir(xdg_base_getter):
    configdir = os.environ.get('MPLCONFIGDIR')
    if configdir:
        configdir = Path(configdir)
    elif sys.platform.startswith(('linux', 'freebsd')):
        # Only call _xdg_base_getter here so that MPLCONFIGDIR is tried first,
        # as _xdg_base_getter can throw.
        try:
            configdir = Path(xdg_base_getter(), "matplotlib")
        except RuntimeError:  # raised if Path.home() is not available
            pass
    elif sys.platform == 'win32':
        # On Windows, prefer %LOCALAPPDATA%\matplotlib which is the proper
        # location for non-roaming application data (cache and config).
        # See: https://docs.microsoft.com/en-us/windows/apps/design/app-settings/store-and-retrieve-app-data
        #
        # However, for backwards compatibility, if the old location
        # (%USERPROFILE%\.matplotlib) exists, continue using it so existing
        # users don't lose their config.
        try:
            old_configdir = Path.home() / ".matplotlib"
            if old_configdir.is_dir():
                configdir = old_configdir
            else:
                localappdata = os.environ.get('LOCALAPPDATA')
                if localappdata:
                    configdir = Path(localappdata) / "matplotlib"
                else:
                    configdir = old_configdir
        except RuntimeError:  # raised if Path.home() is not available
            localappdata = os.environ.get('LOCALAPPDATA')
            if localappdata:
                configdir = Path(localappdata) / "matplotlib"
    else:
        try:
            configdir = Path.home() / ".matplotlib"
        except RuntimeError:  # raised if Path.home() is not available
            pass

    if configdir:
        # Resolve the path to handle potential issues with inaccessible symlinks.
        configdir = configdir.resolve()
        try:
            configdir.mkdir(parents=True, exist_ok=True)
        except OSError as exc:
            _log.warning("mkdir -p failed for path %s: %s", configdir, exc)
        else:
            if os.access(str(configdir), os.W_OK) and configdir.is_dir():
                return str(configdir)
            _log.warning("%s is not a writable directory", configdir)
        issue_msg = "the default path ({configdir})"
    else:
        issue_msg = "resolving the home directory"
    # If the config or cache directory cannot be created or is not a writable
    # directory, create a temporary one.
    try:
        tmpdir = tempfile.mkdtemp(prefix="matplotlib-")
    except OSError as exc:
        raise OSError(
            f"Matplotlib requires access to a writable cache directory, but there "
            f"was an issue with {issue_msg}, and a temporary "
            f"directory could not be created; set the MPLCONFIGDIR environment "
            f"variable to a writable directory") from exc
    os.environ["MPLCONFIGDIR"] = tmpdir
    atexit.register(shutil.rmtree, tmpdir)
    _log.warning(
        "Matplotlib created a temporary cache directory at %s because there was "
        "an issue with %s; it is highly recommended to set the "
        "MPLCONFIGDIR environment variable to a writable directory, in particular to "
        "speed up the import of Matplotlib and to better support multiprocessing.",
        tmpdir, issue_msg)
    return tmpdir

