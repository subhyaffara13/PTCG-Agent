
def site_config_dirs(appname: str) -> list[str]:
    if sys.platform == "darwin":
        dirval = _appdirs.site_data_dir(appname, appauthor=False, multipath=True)
        return dirval.split(os.pathsep)

    dirval = _appdirs.site_config_dir(appname, appauthor=False, multipath=True)
    if sys.platform == "win32":
        return [dirval]

    # Unix-y system. Look in /etc as well.
    return dirval.split(os.pathsep) + ["/etc"]

