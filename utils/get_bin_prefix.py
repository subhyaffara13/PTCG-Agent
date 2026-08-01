
def get_bin_prefix() -> str:
    # XXX: In old virtualenv versions, sys.prefix can contain '..' components,
    # so we need to call normpath to eliminate them.
    prefix = os.path.normpath(sys.prefix)
    if WINDOWS:
        bin_py = os.path.join(prefix, "Scripts")
        # buildout uses 'bin' on Windows too?
        if not os.path.exists(bin_py):
            bin_py = os.path.join(prefix, "bin")
        return bin_py
    # Forcing to use /usr/local/bin for standard macOS framework installs
    # Also log to ~/Library/Logs/ for use with the Console.app log viewer
    if sys.platform[:6] == "darwin" and prefix[:16] == "/System/Library/":
        return "/usr/local/bin"
    return os.path.join(prefix, "bin")


def get_bin_prefix() -> str:
    # Forcing to use /usr/local/bin for standard macOS framework installs.
    if sys.platform[:6] == "darwin" and sys.prefix[:16] == "/System/Library/":
        return "/usr/local/bin"
    return sysconfig.get_paths()["scripts"]


def get_bin_prefix() -> str:
    new = _sysconfig.get_bin_prefix()
    if _USE_SYSCONFIG:
        return new

    old = _distutils.get_bin_prefix()
    if _warn_if_mismatch(pathlib.Path(old), pathlib.Path(new), key="bin_prefix"):
        _log_context()
    return old

